"""
Pydantic schemas for request/response validation
API data transfer objects
"""

import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class VehicleCreate(BaseModel):
    """Schema for vehicle creation request"""
    vin: str = Field(..., min_length=17, max_length=17, description="Vehicle Identification Number")
    model_year: int = Field(..., ge=2008, le=2030, description="Manufacturing year")
    engine_type: Optional[str] = Field(None, max_length=100, description="Engine specification")
    transmission: Optional[str] = Field(None, description="Transmission type")
    
    @validator("vin")
    def validate_vin(cls, v):
        if not v:
            raise ValueError("VIN is required")
        v = v.upper()
        valid_chars = set("ABCDEFGHJKLMNPRSTUVWXYZ0123456789")
        if not all(c in valid_chars for c in v):
            raise ValueError("VIN contains invalid characters (I, O, Q not allowed)")
        return v
    
    @validator("transmission")
    def validate_transmission(cls, v):
        if v and v not in ["manual", "automatic", "cvt"]:
            raise ValueError("Transmission must be 'manual', 'automatic', or 'cvt'")
        return v


class VehicleResponse(BaseModel):
    """Schema for vehicle response"""
    id: uuid.UUID
    vin: str
    model_year: int
    engine_type: Optional[str]
    transmission: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class VehicleListResponse(BaseModel):
    """Schema for vehicle list response"""
    vehicles: List[VehicleResponse]
    total_count: int
    limit: int
    offset: int


class SessionCreate(BaseModel):
    """Schema for diagnostic session creation"""
    connection_method: str = Field(..., description="Connection method")
    adapter_type: str = Field(..., description="Adapter type")
    
    @validator("connection_method")
    def validate_connection_method(cls, v):
        if v not in ["bluetooth", "wifi", "cable"]:
            raise ValueError("Connection method must be 'bluetooth', 'wifi', or 'cable'")
        return v


class SessionResponse(BaseModel):
    """Schema for diagnostic session response"""
    id: uuid.UUID
    vehicle_id: uuid.UUID
    started_at: datetime
    ended_at: Optional[datetime]
    connection_method: str
    adapter_type: str
    status: str
    total_data_points: int
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class SystemDataCreate(BaseModel):
    """Schema for system data creation"""
    timestamp: datetime
    parameter_name: str
    parameter_id: str
    raw_value: str
    converted_value: Optional[float] = None
    unit: Optional[str] = None
    is_error_code: bool = False
    severity_level: Optional[str] = None


class SystemDataBatch(BaseModel):
    """Schema for batch system data submission"""
    data_points: List[SystemDataCreate] = Field(..., min_items=1, max_items=1000)


class SystemDataResponse(BaseModel):
    """Schema for system data response"""
    id: uuid.UUID
    session_id: uuid.UUID
    timestamp: datetime
    parameter_name: str
    parameter_id: str
    raw_value: str
    converted_value: Optional[float]
    unit: Optional[str]
    is_error_code: bool
    severity_level: Optional[str]
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str
    message: str
    details: Optional[dict] = None