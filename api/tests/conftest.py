"""
Pytest configuration and fixtures for Vehicle Diagnostics API tests
Provides common test setup and utilities
"""

import pytest
import os
import sys
from pathlib import Path
from typing import Generator

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import will fail until main app is implemented - this is expected for TDD
try:
    from main import app
    from config.settings import settings
except ImportError:
    # Expected during TDD phase - tests should fail initially
    app = None
    settings = None


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI application"""
    if app is None:
        pytest.skip("Application not implemented yet - TDD phase")
    
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_db():
    """Create a test database session"""
    # Use in-memory SQLite for tests
    test_engine = create_engine("sqlite:///:memory:", echo=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    # Create tables (will need to import models when implemented)
    # Base.metadata.create_all(bind=test_engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_vehicle_data():
    """Sample vehicle data for testing"""
    return {
        "vin": "VF3C9HHZE12345678",
        "model_year": 2020,
        "engine_type": "1.2L PureTech",
        "transmission": "manual"
    }


@pytest.fixture
def sample_session_data():
    """Sample diagnostic session data for testing"""
    return {
        "connection_method": "bluetooth",
        "adapter_type": "ELM327"
    }


@pytest.fixture
def sample_system_data():
    """Sample system data points for testing"""
    return [
        {
            "timestamp": "2025-09-12T10:00:00Z",
            "parameter_name": "ENGINE_LOAD",
            "parameter_id": "01 04",
            "raw_value": "50",
            "converted_value": 19.6,
            "unit": "%",
            "is_error_code": False
        },
        {
            "timestamp": "2025-09-12T10:00:01Z",
            "parameter_name": "SPEED",
            "parameter_id": "01 0D",
            "raw_value": "30",
            "converted_value": 48.0,
            "unit": "km/h",
            "is_error_code": False
        }
    ]


@pytest.fixture
def sample_report_data():
    """Sample report generation data for testing"""
    return {
        "report_type": "fuel_analysis",
        "title": "Fuel Consumption Analysis"
    }