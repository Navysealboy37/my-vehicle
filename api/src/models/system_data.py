"""
SystemData model for storing vehicle diagnostic data points
Represents individual sensor readings and diagnostic parameters
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean, DateTime, Enum as SQLEnum, Float, ForeignKey, String, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, UUIDMixin


class SeverityLevel(str, Enum):
    """Enumeration of data point severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class SystemData(Base, UUIDMixin):
    """System data model for individual diagnostic data points"""
    
    __tablename__ = "system_data"
    
    # Foreign key to diagnostic session
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("diagnostic_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Timestamp when data was collected
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )
    
    # OBD-II parameter name (e.g., "ENGINE_LOAD", "SPEED")
    parameter_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )
    
    # OBD-II PID code (e.g., "01 04", "01 0D")
    parameter_id: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    
    # Raw value from vehicle as string
    raw_value: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )
    
    # Converted/calculated numeric value
    converted_value: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    
    # Unit of measurement (e.g., "km/h", "°C", "%")
    unit: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True
    )
    
    # Whether this represents an error condition
    is_error_code: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    
    # Severity level for error conditions
    severity_level: Mapped[Optional[SeverityLevel]] = mapped_column(
        SQLEnum(SeverityLevel),
        nullable=True
    )
    
    # Relationships
    session: Mapped["DiagnosticSession"] = relationship(
        "DiagnosticSession",
        back_populates="system_data"
    )
    
    def __repr__(self) -> str:
        return (
            f"<SystemData(id={self.id}, parameter={self.parameter_name}, "
            f"value={self.converted_value}, timestamp={self.timestamp})>"
        )
    
    @property
    def formatted_value(self) -> str:
        """Format value with unit for display"""
        if self.converted_value is not None and self.unit:
            return f"{self.converted_value} {self.unit}"
        elif self.converted_value is not None:
            return str(self.converted_value)
        else:
            return self.raw_value
    
    @property
    def is_numeric(self) -> bool:
        """Check if the data point has a numeric value"""
        return self.converted_value is not None
    
    def is_within_normal_range(self) -> Optional[bool]:
        """
        Check if value is within normal operating range
        Returns None if no range is defined for this parameter
        """
        # Define normal ranges for common OBD-II parameters
        normal_ranges = {
            "ENGINE_LOAD": (0, 100),      # %
            "COOLANT_TEMP": (70, 105),    # °C
            "SPEED": (0, 200),            # km/h
            "RPM": (600, 6500),           # rpm
            "THROTTLE_POS": (0, 100),     # %
            "FUEL_LEVEL": (0, 100),       # %
            "MAF": (0, 500),              # g/s
        }
        
        if (self.parameter_name in normal_ranges and 
            self.converted_value is not None):
            min_val, max_val = normal_ranges[self.parameter_name]
            return min_val <= self.converted_value <= max_val
        
        return None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "timestamp": self.timestamp.isoformat(),
            "parameter_name": self.parameter_name,
            "parameter_id": self.parameter_id,
            "raw_value": self.raw_value,
            "converted_value": self.converted_value,
            "unit": self.unit,
            "is_error_code": self.is_error_code,
            "severity_level": self.severity_level.value if self.severity_level else None
        }