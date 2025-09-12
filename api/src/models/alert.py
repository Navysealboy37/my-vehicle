"""
Alert model for storing vehicle diagnostic alerts and notifications
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class AlertType(str, Enum):
    """Types of diagnostic alerts"""
    ERROR_CODE = "error_code"
    MAINTENANCE = "maintenance"
    PERFORMANCE = "performance"
    SAFETY = "safety"


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Alert(Base, UUIDMixin, TimestampMixin):
    """Alert model for vehicle diagnostic notifications"""
    
    __tablename__ = "alerts"
    
    vehicle_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("vehicles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    report_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reports.id", ondelete="SET NULL"),
        nullable=True
    )
    
    alert_type: Mapped[AlertType] = mapped_column(
        SQLEnum(AlertType),
        nullable=False
    )
    
    severity: Mapped[AlertSeverity] = mapped_column(
        SQLEnum(AlertSeverity),
        nullable=False,
        index=True
    )
    
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    recommended_action: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    is_acknowledged: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True
    )
    
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Relationships
    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        back_populates="alerts"
    )
    
    report: Mapped[Optional["Report"]] = relationship(
        "Report",
        back_populates="alerts"
    )
    
    def acknowledge(self) -> None:
        """Mark alert as acknowledged"""
        if not self.is_acknowledged:
            self.is_acknowledged = True
            self.acknowledged_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "vehicle_id": str(self.vehicle_id),
            "report_id": str(self.report_id) if self.report_id else None,
            "alert_type": self.alert_type.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "recommended_action": self.recommended_action,
            "is_acknowledged": self.is_acknowledged,
            "created_at": self.created_at.isoformat(),
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }