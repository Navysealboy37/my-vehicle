"""
Vehicle API endpoints
Handles vehicle registration, retrieval, and management
"""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import (
    VehicleCreate, VehicleResponse, VehicleListResponse, ErrorResponse
)
from ..services.vehicle_service import VehicleService

router = APIRouter(prefix="/api/v1", tags=["vehicles"])


@router.post(
    "/vehicles",
    response_model=VehicleResponse,
    status_code=201,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        409: {"model": ErrorResponse, "description": "Vehicle with VIN already exists"}
    }
)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db)
) -> VehicleResponse:
    """Register a new Peugeot 2008 vehicle for diagnostic monitoring"""
    service = VehicleService(db)
    
    try:
        vehicle = service.create_vehicle(
            vin=vehicle_data.vin,
            model_year=vehicle_data.model_year,
            engine_type=vehicle_data.engine_type,
            transmission=vehicle_data.transmission
        )
        return VehicleResponse.from_orm(vehicle)
    except ValueError as e:
        if "already exists" in str(e):
            raise HTTPException(
                status_code=409,
                detail={"error": "Conflict", "message": str(e)}
            )
        else:
            raise HTTPException(
                status_code=400,
                detail={"error": "Bad Request", "message": str(e)}
            )


@router.get(
    "/vehicles",
    response_model=VehicleListResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid pagination parameters"}
    }
)
async def list_vehicles(
    limit: int = Query(20, ge=1, le=100, description="Maximum number of vehicles to return"),
    offset: int = Query(0, ge=0, description="Number of vehicles to skip"),
    db: Session = Depends(get_db)
) -> VehicleListResponse:
    """Retrieve a paginated list of registered vehicles"""
    service = VehicleService(db)
    
    try:
        vehicles, total_count = service.get_vehicles(limit=limit, offset=offset)
        return VehicleListResponse(
            vehicles=[VehicleResponse.from_orm(v) for v in vehicles],
            total_count=total_count,
            limit=limit,
            offset=offset
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": "Bad Request", "message": str(e)}
        )


@router.get(
    "/vehicles/{vehicle_id}",
    response_model=VehicleResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid vehicle ID format"},
        404: {"model": ErrorResponse, "description": "Vehicle not found"}
    }
)
async def get_vehicle(
    vehicle_id: uuid.UUID,
    db: Session = Depends(get_db)
) -> VehicleResponse:
    """Retrieve detailed information about a specific vehicle"""
    service = VehicleService(db)
    
    try:
        vehicle = service.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(
                status_code=404,
                detail={"error": "Not Found", "message": f"Vehicle with ID {vehicle_id} not found"}
            )
        
        return VehicleResponse.from_orm(vehicle)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": "Bad Request", "message": "Invalid vehicle ID format"}
        )