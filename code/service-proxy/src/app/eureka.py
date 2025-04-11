import os
from py_eureka_client import eureka_client
from fastapi import FastAPI
from config.settings import Settings

settings = Settings()

async def register_with_eureka(app: FastAPI):
    await eureka_client.init_async(
        eureka_server=f"{settings.eureka_url}",
        app_name=settings.app_name,
        instance_port=settings.app_port,
        instance_host=settings.app_host,
        renewal_interval_in_secs=30,
        duration_in_secs=90,
        metadata={
            "zone": "primary",
            "securePortEnabled": "false",
            "securePort": "443",
            "statusPageUrl": f"http://{settings.app_host}:{settings.app_port}/info",
            "healthCheckUrl": f"http://{settings.app_host}:{settings.app_port}/health"
        }
    )

async def shutdown_eureka():
    await eureka_client.stop_async()