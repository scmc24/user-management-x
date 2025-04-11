from fastapi import APIRouter, HTTPException, Request, Response
import aiohttp
from py_eureka_client import eureka_client
from config.settings import Settings
import logging
import random
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from collections import defaultdict
import json
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

# Set up logging
logger = logging.getLogger(__name__)
router = APIRouter()
settings = Settings()

# Configuration
REQUEST_TIMEOUT = 10  # seconds
PROXY_RESERVED_PARAMS = {'lb_strategy'}  # Parameters the proxy uses internally

@dataclass
class ServiceInstance:
    hostName: str
    port: dict
    last_used: float = 0
    request_count: int = 0
    error_count: int = 0

class LoadBalancer:
    def __init__(self):
        self.instance_stats = defaultdict(dict)
        self._round_robin_index = defaultdict(int)
    
    def get_instance(self, instances: List[ServiceInstance], strategy: str = "round_robin") -> Optional[ServiceInstance]:
        """Select an instance based on the specified strategy"""
        if not instances:
            return None
            
        if strategy == "random":
            return random.choice(instances)
            
        elif strategy == "round_robin":
            idx = self._round_robin_index[str(id(instances))] % len(instances)
            self._round_robin_index[str(id(instances))] += 1
            return instances[idx]
            
        elif strategy == "least_connections":
            return min(instances, key=lambda x: x.request_count)
            
        return instances[0]  # Default to first instance

load_balancer = LoadBalancer()

async def format_response(response: aiohttp.ClientResponse) -> Dict[str, Any]:
    """Format the response from the target service into a consistent JSON structure"""
    try:
        content_type = response.headers.get('Content-Type', '').lower()
        
        if 'application/json' in content_type:
            return await response.json()
        else:
            text = await response.text()
            try:
                # Try to parse as JSON if not explicitly JSON content-type
                return json.loads(text)
            except json.JSONDecodeError:
                # Format non-JSON responses as JSON
                return {
                    "content": text,
                    "content_type": content_type,
                    "original_status": response.status
                }
    except Exception as e:
        logger.error(f"Error formatting response: {str(e)}")
        return {"error": "response_format_error", "details": str(e)}

def prepare_target_url(path: str, query_params: Dict[str, List[str]]) -> str:
    """Prepare the target URL by filtering out proxy-specific parameters"""
    filtered_params = {
        k: v for k, v in query_params.items() 
        if k not in PROXY_RESERVED_PARAMS
    }
    query_string = urlencode(filtered_params, doseq=True)
    return f"{path}?{query_string}" if query_string else path

async def forward_request(
    method: str,
    service_name: str,
    path: str,
    request: Request,
    lb_strategy: Optional[str] = "round_robin"
) -> Response:
    """Core request forwarding logic"""
    try:
        # Parse and prepare the request
        parsed_url = urlparse(str(request.url))
        query_params = parse_qs(parsed_url.query)
        modified_path = parsed_url.path.replace(f"/{service_name}", "", 1)
        
        # Get service instances from Eureka
        client = eureka_client.get_client()
        app = client.applications.get_application(service_name.upper())
        raw_instances = app.up_instances
        
        if not raw_instances:
            logger.error(f"No instances available for service: {service_name}")
            raise HTTPException(
                status_code=404,
                detail={"error": "service_unavailable", "service": service_name}
            )
        
        # Prepare instances for load balancing
        instances = [
            ServiceInstance(
                hostName=instance.hostName,
                port=instance.port,
                last_used=load_balancer.instance_stats[instance.hostName].get('last_used', 0),
                request_count=load_balancer.instance_stats[instance.hostName].get('request_count', 0)
            )
            for instance in raw_instances
        ]
        
        # Select instance using load balancer
        instance = load_balancer.get_instance(instances, lb_strategy)
        if not instance:
            raise HTTPException(
                status_code=503,
                detail={"error": "no_available_instances", "service": service_name}
            )
        
        # Update instance statistics
        instance.request_count += 1
        instance.last_used = time.time()
        load_balancer.instance_stats[instance.hostName] = {
            'last_used': instance.last_used,
            'request_count': instance.request_count
        }
        
        logger.info(f"Routing {method} to {instance.hostName} using {lb_strategy}")
        
        # Build target URL with forwarded query parameters
        target_url = f"http://{instance.hostName}:{instance.port.port}{prepare_target_url(modified_path, query_params)}"
        
        # Forward headers (excluding those that shouldn't be forwarded)
        headers = {
            k: v for k, v in request.headers.items()
            if k.lower() not in ['host', 'content-length']
        }
        headers.update({
            "X-Forwarded-For": request.client.host,
            "X-Proxy-LB-Strategy": lb_strategy,
            "X-Proxy-Target-Instance": instance.hostName
        })
        
        # Get request body if present
        body = None
        if method in ['POST', 'PUT', 'PATCH']:
            try:
                body = await request.json()
            except:
                body = await request.body()
        
        # Make the proxied request
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method,
                    target_url,
                    headers=headers,
                    json=body if isinstance(body, dict) else None,
                    data=body if not isinstance(body, dict) else None,
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                ) as response:
                    
                    # Format the response from the target service
                    response_data = await format_response(response)
                    
                    # Prepare the complete response with metadata
                    complete_response = {
                        "data": response_data,
                        "metadata": {
                            "service": service_name,
                            "instance": instance.hostName,
                            "strategy": lb_strategy,
                            "status": response.status,
                            "proxy_timestamp": time.time(),
                            "forwarded_query_params": prepare_target_url("", query_params)[1:]  # Remove leading ?
                        }
                    }
                    
                    # Return as JSON response
                    return Response(
                        content=json.dumps(complete_response, ensure_ascii=False),
                        media_type="application/json",
                        status_code=response.status
                    )
                    
            except aiohttp.ClientError as e:
                instance.error_count += 1
                logger.error(f"Request to {instance.hostName} failed: {str(e)}")
                error_response = {
                    "error": "bad_gateway",
                    "service": service_name,
                    "instance": instance.hostName,
                    "details": str(e)
                }
                return Response(
                    content=json.dumps(error_response, ensure_ascii=False),
                    media_type="application/json",
                    status_code=502
                )
                
    except HTTPException as he:
        # Re-raise existing HTTPExceptions
        raise he
    except Exception as e:
        logger.exception(f"Unexpected proxy error: {str(e)}")
        error_response = {
            "error": "internal_server_error",
            "details": str(e)
        }
        return Response(
            content=json.dumps(error_response, ensure_ascii=False),
            media_type="application/json",
            status_code=500
        )

# GET endpoint
@router.get("/{service_name}/{path:path}")
async def proxy_get(
    service_name: str, 
    path: str,
    request: Request,
    lb_strategy: Optional[str] = "round_robin"
) -> Response:
    """Proxy GET requests"""
    return await forward_request("GET", service_name, path, request, lb_strategy)

# POST endpoint
@router.post("/{service_name}/{path:path}")
async def proxy_post(
    service_name: str, 
    path: str,
    request: Request,
    lb_strategy: Optional[str] = "round_robin"
) -> Response:
    """Proxy POST requests"""
    return await forward_request("POST", service_name, path, request, lb_strategy)

# PUT endpoint
@router.put("/{service_name}/{path:path}")
async def proxy_put(
    service_name: str, 
    path: str,
    request: Request,
    lb_strategy: Optional[str] = "round_robin"
) -> Response:
    """Proxy PUT requests"""
    return await forward_request("PUT", service_name, path, request, lb_strategy)

# DELETE endpoint
@router.delete("/{service_name}/{path:path}")
async def proxy_delete(
    service_name: str, 
    path: str,
    request: Request,
    lb_strategy: Optional[str] = "round_robin"
) -> Response:
    """Proxy DELETE requests"""
    return await forward_request("DELETE", service_name, path, request, lb_strategy)