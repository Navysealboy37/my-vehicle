"""
Contract test for POST /api/v1/vehicles endpoint
Tests vehicle registration functionality according to OpenAPI specification

This test MUST FAIL initially - it's part of TDD approach.
Implementation will be created after all tests are written.
"""

import pytest
from fastapi.testclient import TestClient


class TestVehiclesPostContract:
    """Contract tests for vehicle registration endpoint"""
    
    def test_post_vehicles_success(self, test_client: TestClient, sample_vehicle_data):
        """Test successful vehicle registration"""
        response = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        
        # Contract assertions based on OpenAPI spec
        assert response.status_code == 201
        
        response_data = response.json()
        assert "id" in response_data
        assert response_data["vin"] == sample_vehicle_data["vin"]
        assert response_data["model_year"] == sample_vehicle_data["model_year"]
        assert response_data["engine_type"] == sample_vehicle_data["engine_type"]
        assert response_data["transmission"] == sample_vehicle_data["transmission"]
        assert "created_at" in response_data
        assert "updated_at" in response_data
        
        # Validate UUID format for id
        import uuid
        assert uuid.UUID(response_data["id"])
    
    def test_post_vehicles_duplicate_vin(self, test_client: TestClient, sample_vehicle_data):
        """Test vehicle registration with duplicate VIN should return 409"""
        # First registration
        response1 = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        assert response1.status_code == 201
        
        # Duplicate registration
        response2 = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        assert response2.status_code == 409
        
        error_data = response2.json()
        assert "error" in error_data
        assert "message" in error_data
        assert "VIN already exists" in error_data["message"]
    
    def test_post_vehicles_invalid_vin(self, test_client: TestClient, sample_vehicle_data):
        """Test vehicle registration with invalid VIN format"""
        invalid_data = sample_vehicle_data.copy()
        invalid_data["vin"] = "INVALID_VIN"  # Too short
        
        response = test_client.post("/api/v1/vehicles", json=invalid_data)
        assert response.status_code == 400
        
        error_data = response.json()
        assert "error" in error_data
        assert "VIN must be exactly 17 characters" in error_data["message"]
    
    def test_post_vehicles_invalid_model_year(self, test_client: TestClient, sample_vehicle_data):
        """Test vehicle registration with invalid model year"""
        invalid_data = sample_vehicle_data.copy()
        invalid_data["model_year"] = 2050  # Future year
        
        response = test_client.post("/api/v1/vehicles", json=invalid_data)
        assert response.status_code == 400
        
        error_data = response.json()
        assert "error" in error_data
    
    def test_post_vehicles_missing_required_fields(self, test_client: TestClient):
        """Test vehicle registration with missing required fields"""
        incomplete_data = {
            "vin": "VF3C9HHZE12345678"
            # Missing model_year
        }
        
        response = test_client.post("/api/v1/vehicles", json=incomplete_data)
        assert response.status_code == 400
        
        error_data = response.json()
        assert "error" in error_data
    
    def test_post_vehicles_invalid_transmission(self, test_client: TestClient, sample_vehicle_data):
        """Test vehicle registration with invalid transmission type"""
        invalid_data = sample_vehicle_data.copy()
        invalid_data["transmission"] = "invalid_type"
        
        response = test_client.post("/api/v1/vehicles", json=invalid_data)
        assert response.status_code == 400
        
        error_data = response.json()
        assert "error" in error_data
    
    def test_post_vehicles_optional_fields(self, test_client: TestClient):
        """Test vehicle registration with only required fields"""
        minimal_data = {
            "vin": "VF3C9HHZE12345679",
            "model_year": 2019
        }
        
        response = test_client.post("/api/v1/vehicles", json=minimal_data)
        assert response.status_code == 201
        
        response_data = response.json()
        assert response_data["vin"] == minimal_data["vin"]
        assert response_data["model_year"] == minimal_data["model_year"]
        assert response_data["engine_type"] is None
        assert response_data["transmission"] is None