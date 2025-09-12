"""
FastAPI application for Vehicle Diagnostics API
Handles Peugeot 2008 diagnostic data collection and mobile reporting
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.vehicles import router as vehicles_router
from .database import create_tables
from config.settings import settings

# Create database tables on startup
create_tables()

app = FastAPI(
    title=settings.api.title,
    description=settings.api.description,
    version=settings.api.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for mobile app access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.api.allowed_methods,
    allow_headers=settings.api.allowed_headers,
)

# Include API routers
app.include_router(vehicles_router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Vehicle Diagnostics API", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check for monitoring"""
    return {
        "status": "healthy",
        "version": settings.api.version,
        "service": "vehicle-diagnostics-api",
        "environment": settings.environment
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.api.host, 
        port=settings.api.port,
        reload=settings.api.reload
    )