"""
DiagnosticSession model for storing vehicle diagnostic session information
Represents a single troubleshooting session with timestamps and connection status
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import (
    DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class SessionStatus(str, Enum):
    """Enumeration of possible session statuses"""
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    INTERRUPTED = "interrupted"


class ConnectionMethod(str, Enum):
    """Enumeration of connection methods"""
    BLUETOOTH = "bluetooth"
    WIFI = "wifi"
    CABLE = "cable"


class DiagnosticSession(Base, UUIDMixin, TimestampMixin):
    """Diagnostic session model for tracking vehicle diagnostic activities"""
    
    __tablename__ = "diagnostic_sessions"
    
    # Foreign key to vehicle
    vehicle_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("vehicles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Session start timestamp
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )
    
    # Session end timestamp (nullable for active sessions)
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Connection method used
    connection_method: Mapped[ConnectionMethod] = mapped_column(
        SQLEnum(ConnectionMethod),
        nullable=False
    )
    
    # Adapter type (e.g., "ELM327")
    adapter_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
    # Current session status
    status: Mapped[SessionStatus] = mapped_column(
        SQLEnum(SessionStatus),
        nullable=False,
        default=SessionStatus.ACTIVE,
        index=True
    )
    
    # Total number of data points collected
    total_data_points: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    
    # Error message for failed sessions
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    # Relationships
    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        back_populates="diagnostic_sessions"
    )
    
    system_data: Mapped[List["SystemData"]] = relationship(
        "SystemData",
        back_populates="session",
        cascade="all, delete-orphan"
    )
    
    reports: Mapped[List["Report"]] = relationship(
        "Report",
        back_populates="session",
        cascade="all, delete-orphan"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "ended_at IS NULL OR ended_at >= started_at",
            name="valid_end_time"
        ),
        CheckConstraint(
            "total_data_points >= 0",
            name="non_negative_data_points"
        ),
        CheckConstraint(
            "(status = 'failed' AND error_message IS NOT NULL) OR "
            "(status != 'failed' AND error_message IS NULL)",
            name="error_message_required_for_failed"
        ),
    )
    
    def __repr__(self) -> str:
        return (
            f"<DiagnosticSession(id={self.id}, vehicle_id={self.vehicle_id}, "
            f"status={self.status}, started_at={self.started_at})>"
        )
    
    @property
    def duration(self) -> Optional[float]:
        """Calculate session duration in seconds"""
        if self.ended_at:
            return (self.ended_at - self.started_at).total_seconds()
        elif self.status == SessionStatus.ACTIVE:
            return (datetime.utcnow() - self.started_at).total_seconds()
        return None
    
    @property
    def is_active(self) -> bool:
        """Check if session is currently active"""
        return self.status == SessionStatus.ACTIVE
    
    @property
    def can_add_data(self) -> bool:
        """Check if session can accept new data points"""
        return self.status == SessionStatus.ACTIVE
    
    def complete_session(self) -> None:
        """Mark session as completed"""
        if self.status == SessionStatus.ACTIVE:
            self.status = SessionStatus.COMPLETED
            self.ended_at = datetime.utcnow()
    
    def fail_session(self, error_message: str) -> None:
        """Mark session as failed with error message"""
        if self.status == SessionStatus.ACTIVE:
            self.status = SessionStatus.FAILED
            self.ended_at = datetime.utcnow()
            self.error_message = error_message
    
    def interrupt_session(self) -> None:
        """Mark session as interrupted (user cancellation)"""
        if self.status == SessionStatus.ACTIVE:
            self.status = SessionStatus.INTERRUPTED
            self.ended_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": str(self.id),
            "vehicle_id": str(self.vehicle_id),
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "connection_method": self.connection_method.value,
            "adapter_type": self.adapter_type,
            "status": self.status.value,
            "total_data_points": self.total_data_points,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat()
        }