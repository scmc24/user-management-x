from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from eureka import register_with_eureka, shutdown_eureka
from proxy.routes import router as proxy_router
from config.settings import Settings

settings = Settings()

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(proxy_router)

# Eureka lifecycle events
@app.on_event("startup")
async def startup_event():
    await register_with_eureka(app)

@app.on_event("shutdown")
async def shutdown_event():
    await shutdown_eureka()

# Health endpoints
@app.get("/health")
def health_check():
    return {"status": "UP"}

@app.get("/info")
def info():
    return {
        "app": settings.app_name,
        "version": app.version
    }