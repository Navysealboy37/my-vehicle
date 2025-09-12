"""
Vehicle service for CRUD operations and business logic
Handles vehicle registration, retrieval, and management
"""

import uuid
from typing import List, Optional, Tuple
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from ..models.vehicle import Vehicle


class VehicleService:
    """Service for vehicle-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_vehicle(
        self,
        vin: str,
        model_year: int,
        engine_type: Optional[str] = None,
        transmission: Optional[str] = None
    ) -> Vehicle:
        """
        Create a new vehicle record
        
        Args:
            vin: Vehicle Identification Number (17 characters)
            model_year: Manufacturing year
            engine_type: Optional engine specification
            transmission: Optional transmission type
            
        Returns:
            Created Vehicle instance
            
        Raises:
            ValueError: If VIN format is invalid or already exists
            IntegrityError: If database constraints are violated
        """
        # Validate VIN format
        if not vin or len(vin) != 17:
            raise ValueError("VIN must be exactly 17 characters")
        
        # Normalize VIN to uppercase
        vin = vin.upper()
        
        # Validate VIN characters (no I, O, Q allowed in VIN)
        valid_chars = set("ABCDEFGHJKLMNPRSTUVWXYZ0123456789")
        if not all(c in valid_chars for c in vin):
            raise ValueError("VIN contains invalid characters")
        
        # Validate model year
        current_year = datetime.now().year
        if model_year < 2008 or model_year > current_year + 1:
            raise ValueError(f"Model year must be between 2008 and {current_year + 1}")
        
        # Validate transmission type if provided
        if transmission and transmission not in ["manual", "automatic", "cvt"]:
            raise ValueError("Transmission must be 'manual', 'automatic', or 'cvt'")
        
        # Check if VIN already exists
        existing_vehicle = self.db.query(Vehicle).filter(Vehicle.vin == vin).first()
        if existing_vehicle:
            raise ValueError(f"Vehicle with VIN {vin} already exists")
        
        # Create new vehicle
        vehicle = Vehicle(
            vin=vin,
            model_year=model_year,
            engine_type=engine_type,
            transmission=transmission
        )
        
        try:
            self.db.add(vehicle)
            self.db.commit()
            self.db.refresh(vehicle)
            return vehicle
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Failed to create vehicle: {str(e)}")
    
    def get_vehicle_by_id(self, vehicle_id: uuid.UUID) -> Optional[Vehicle]:
        """
        Retrieve vehicle by ID
        
        Args:
            vehicle_id: Vehicle UUID
            
        Returns:
            Vehicle instance if found, None otherwise
        """
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    
    def get_vehicle_by_vin(self, vin: str) -> Optional[Vehicle]:
        """
        Retrieve vehicle by VIN
        
        Args:
            vin: Vehicle Identification Number
            
        Returns:
            Vehicle instance if found, None otherwise
        """
        return self.db.query(Vehicle).filter(Vehicle.vin == vin.upper()).first()
    
    def get_vehicles(
        self,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[Vehicle], int]:
        """
        Retrieve paginated list of vehicles
        
        Args:
            limit: Maximum number of vehicles to return (1-100)
            offset: Number of vehicles to skip
            
        Returns:
            Tuple of (vehicles list, total count)
            
        Raises:
            ValueError: If pagination parameters are invalid
        """
        # Validate pagination parameters
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")
        
        if offset < 0:
            raise ValueError("Offset must be non-negative")
        
        # Get total count
        total_count = self.db.query(func.count(Vehicle.id)).scalar()
        
        # Get paginated vehicles
        vehicles = (
            self.db.query(Vehicle)
            .order_by(Vehicle.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        return vehicles, total_count
    
    def update_vehicle(
        self,
        vehicle_id: uuid.UUID,
        engine_type: Optional[str] = None,
        transmission: Optional[str] = None
    ) -> Optional[Vehicle]:
        """
        Update vehicle information (VIN and model_year are immutable)
        
        Args:
            vehicle_id: Vehicle UUID
            engine_type: New engine type
            transmission: New transmission type
            
        Returns:
            Updated Vehicle instance if found, None otherwise
            
        Raises:
            ValueError: If transmission type is invalid
        """
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            return None
        
        # Validate transmission type if provided
        if transmission and transmission not in ["manual", "automatic", "cvt"]:
            raise ValueError("Transmission must be 'manual', 'automatic', or 'cvt'")
        
        # Update fields
        if engine_type is not None:
            vehicle.engine_type = engine_type
        
        if transmission is not None:
            vehicle.transmission = transmission
        
        # Commit changes
        self.db.commit()
        self.db.refresh(vehicle)
        
        return vehicle
    
    def delete_vehicle(self, vehicle_id: uuid.UUID) -> bool:
        """
        Delete vehicle and all associated data
        
        Args:
            vehicle_id: Vehicle UUID
            
        Returns:
            True if vehicle was deleted, False if not found
        """
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            return False
        
        self.db.delete(vehicle)
        self.db.commit()
        
        return True
    
    def get_vehicle_stats(self, vehicle_id: uuid.UUID) -> Optional[dict]:
        """
        Get statistics for a vehicle
        
        Args:
            vehicle_id: Vehicle UUID
            
        Returns:
            Dictionary with vehicle statistics or None if not found
        """
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            return None
        
        # Count related entities
        session_count = len(vehicle.diagnostic_sessions)
        alert_count = len([alert for alert in vehicle.alerts if not alert.is_acknowledged])
        
        return {
            "vehicle_id": str(vehicle.id),
            "total_sessions": session_count,
            "active_alerts": alert_count,
            "last_session": (
                vehicle.diagnostic_sessions[-1].started_at.isoformat()
                if vehicle.diagnostic_sessions
                else None
            )
        }