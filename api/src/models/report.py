"""
Report model for storing generated diagnostic reports
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class ReportType(str, Enum):
    """Types of diagnostic reports"""
    SUMMARY = "summary"
    FUEL_ANALYSIS = "fuel_analysis"
    ERROR_ANALYSIS = "error_analysis"
    MAINTENANCE = "maintenance"


class ReportStatus(str, Enum):
    """Report generation status"""
    GENERATING = "generating"
    READY = "ready"
    ARCHIVED = "archived"


class Report(Base, UUIDMixin, TimestampMixin):
    """Report model for diagnostic analysis results"""
    
    __tablename__ = "reports"
    
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("diagnostic_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    report_type: Mapped[ReportType] = mapped_column(
        SQLEnum(ReportType),
        nullable=False
    )
    
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    
    summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    recommendations: Mapped[Optional[Dict]] = mapped_column(
        JSON,
        nullable=True
    )
    
    charts_config: Mapped[Optional[Dict]] = mapped_column(
        JSON,
        nullable=True
    )
    
    data_points_analyzed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    
    status: Mapped[ReportStatus] = mapped_column(
        SQLEnum(ReportStatus),
        nullable=False,
        default=ReportStatus.GENERATING
    )
    
    # Relationships
    session: Mapped["DiagnosticSession"] = relationship(
        "DiagnosticSession",
        back_populates="reports"
    )
    
    alerts: Mapped[List["Alert"]] = relationship(
        "Alert",
        back_populates="report"
    )
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "report_type": self.report_type.value,
            "title": self.title,
            "generated_at": self.generated_at.isoformat(),
            "summary": self.summary,
            "recommendations": self.recommendations,
            "charts_config": self.charts_config,
            "data_points_analyzed": self.data_points_analyzed,
            "status": self.status.value
        }