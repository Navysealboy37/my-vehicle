"""
Database configuration and session management
SQLAlchemy setup for Vehicle Diagnostics API
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from config.settings import settings
from .models import Base

# Create database engine
engine = create_engine(
    settings.database.url,
    # For SQLite
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database.url else {},
    echo=settings.debug
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """
    Dependency to get database session
    For use with FastAPI dependency injection
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()