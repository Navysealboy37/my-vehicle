"""
MobileDevice model for mobile app device registration and management
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, UUIDMixin


class Platform(str, Enum):
    """Mobile device platforms"""
    IOS = "ios"
    ANDROID = "android"


class MobileDevice(Base, UUIDMixin, TimestampMixin):
    """Mobile device model for push notifications and app management"""
    
    __tablename__ = "mobile_devices"
    
    device_token: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
        index=True
    )
    
    platform: Mapped[Platform] = mapped_column(
        SQLEnum(Platform),
        nullable=False
    )
    
    app_version: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    
    os_version: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    
    last_active: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    
    notification_preferences: Mapped[Optional[Dict]] = mapped_column(
        JSON,
        nullable=True
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "device_token": self.device_token,
            "platform": self.platform.value,
            "app_version": self.app_version,
            "os_version": self.os_version,
            "last_active": self.last_active.isoformat(),
            "notification_preferences": self.notification_preferences,
            "is_active": self.is_active
        }