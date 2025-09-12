"""
API endpoints for Vehicle Diagnostics API
FastAPI router modules
"""

from .vehicles import router as vehicles_router

__all__ = ["vehicles_router"]