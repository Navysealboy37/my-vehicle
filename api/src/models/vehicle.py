"""
Vehicle model for storing Peugeot 2008 vehicle information
Represents a vehicle with diagnostic capabilities
"""

import re
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Vehicle(Base, UUIDMixin, TimestampMixin):
    """Vehicle model for diagnostic data collection"""
    
    __tablename__ = "vehicles"
    
    # Vehicle Identification Number (VIN) - exactly 17 characters
    vin: Mapped[str] = mapped_column(
        String(17),
        unique=True,
        nullable=False,
        index=True
    )
    
    # Manufacturing year
    model_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )
    
    # Optional engine specification
    engine_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    # Optional transmission type
    transmission: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True
    )
    
    # Relationships
    diagnostic_sessions: Mapped[List["DiagnosticSession"]] = relationship(
        "DiagnosticSession",
        back_populates="vehicle",
        cascade="all, delete-orphan"
    )
    
    alerts: Mapped[List["Alert"]] = relationship(
        "Alert",
        back_populates="vehicle",
        cascade="all, delete-orphan"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "model_year >= 2008 AND model_year <= 2030",
            name="valid_model_year"
        ),
        CheckConstraint(
            "transmission IN ('manual', 'automatic', 'cvt') OR transmission IS NULL",
            name="valid_transmission"
        ),
        CheckConstraint(
            "LENGTH(vin) = 17",
            name="valid_vin_length"
        ),
    )
    
    def __repr__(self) -> str:
        return f"<Vehicle(id={self.id}, vin={self.vin}, year={self.model_year})>"
    
    @property
    def display_name(self) -> str:
        """Human-readable vehicle identifier"""
        return f"Peugeot 2008 {self.model_year} ({self.vin[-6:]})"
    
    def validate_vin(self) -> bool:
        """Validate VIN format according to ISO 3779 standard"""
        if not self.vin or len(self.vin) != 17:
            return False
        
        # VIN should be alphanumeric, no I, O, Q
        valid_chars = set("ABCDEFGHJKLMNPRSTUVWXYZ0123456789")
        return all(c in valid_chars for c in self.vin.upper())
    
    def is_peugeot_2008(self) -> bool:
        """Check if VIN indicates this is a Peugeot 2008"""
        # Peugeot VINs typically start with VF3 for French production
        # This is a simplified check - actual VIN decoding is more complex
        return self.vin.startswith(("VF3", "VF1")) if self.vin else False
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": str(self.id),
            "vin": self.vin,
            "model_year": self.model_year,
            "engine_type": self.engine_type,
            "transmission": self.transmission,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }