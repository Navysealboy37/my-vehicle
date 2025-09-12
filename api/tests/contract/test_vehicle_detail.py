"""
Contract test for GET /api/v1/vehicles/{vehicleId} endpoint
Tests individual vehicle retrieval functionality according to OpenAPI specification

This test MUST FAIL initially - it's part of TDD approach.
Implementation will be created after all tests are written.
"""

import pytest
from fastapi.testclient import TestClient


class TestVehicleDetailContract:
    """Contract tests for individual vehicle retrieval endpoint"""
    
    def test_get_vehicle_success(self, test_client: TestClient, sample_vehicle_data):
        """Test successful retrieval of vehicle details"""
        # First register a vehicle
        post_response = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        assert post_response.status_code == 201
        vehicle_id = post_response.json()["id"]
        
        # Then retrieve vehicle details
        response = test_client.get(f"/api/v1/vehicles/{vehicle_id}")
        assert response.status_code == 200
        
        vehicle_data = response.json()
        assert vehicle_data["id"] == vehicle_id
        assert vehicle_data["vin"] == sample_vehicle_data["vin"]
        assert vehicle_data["model_year"] == sample_vehicle_data["model_year"]
        assert vehicle_data["engine_type"] == sample_vehicle_data["engine_type"]
        assert vehicle_data["transmission"] == sample_vehicle_data["transmission"]
        assert "created_at" in vehicle_data
        assert "updated_at" in vehicle_data
    
    def test_get_vehicle_not_found(self, test_client: TestClient):
        """Test retrieval of non-existent vehicle returns 404"""
        non_existent_id = "550e8400-e29b-41d4-a716-446655440000"
        
        response = test_client.get(f"/api/v1/vehicles/{non_existent_id}")
        assert response.status_code == 404
        
        error_data = response.json()
        assert "error" in error_data
        assert "message" in error_data
        assert "not found" in error_data["message"].lower()
    
    def test_get_vehicle_invalid_uuid_format(self, test_client: TestClient):
        """Test retrieval with invalid UUID format"""
        invalid_id = "not-a-valid-uuid"
        
        response = test_client.get(f"/api/v1/vehicles/{invalid_id}")
        assert response.status_code == 400
        
        error_data = response.json()
        assert "error" in error_data
        assert "invalid" in error_data["message"].lower()
    
    def test_get_vehicle_response_schema(self, test_client: TestClient, sample_vehicle_data):
        """Test that vehicle detail response matches expected schema"""
        # Register a vehicle first
        post_response = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        assert post_response.status_code == 201
        vehicle_id = post_response.json()["id"]
        
        response = test_client.get(f"/api/v1/vehicles/{vehicle_id}")
        assert response.status_code == 200
        
        vehicle_data = response.json()
        
        # Validate required fields
        required_fields = ["id", "vin", "model_year", "created_at", "updated_at"]
        for field in required_fields:
            assert field in vehicle_data
        
        # Validate field types
        import uuid
        assert uuid.UUID(vehicle_data["id"])  # Valid UUID
        assert isinstance(vehicle_data["vin"], str)
        assert len(vehicle_data["vin"]) == 17
        assert isinstance(vehicle_data["model_year"], int)
        assert vehicle_data["model_year"] >= 2008
        
        # Optional fields should be present but may be null
        optional_fields = ["engine_type", "transmission"]
        for field in optional_fields:
            assert field in vehicle_data
    
    def test_get_vehicle_with_optional_fields_null(self, test_client: TestClient):
        """Test vehicle retrieval when optional fields are null"""
        minimal_data = {
            "vin": "VF3C9HHZE12345679",
            "model_year": 2019
        }
        
        # Register vehicle with minimal data
        post_response = test_client.post("/api/v1/vehicles", json=minimal_data)
        assert post_response.status_code == 201
        vehicle_id = post_response.json()["id"]
        
        # Retrieve vehicle
        response = test_client.get(f"/api/v1/vehicles/{vehicle_id}")
        assert response.status_code == 200
        
        vehicle_data = response.json()
        assert vehicle_data["vin"] == minimal_data["vin"]
        assert vehicle_data["model_year"] == minimal_data["model_year"]
        assert vehicle_data["engine_type"] is None
        assert vehicle_data["transmission"] is None
    
    def test_get_vehicle_datetime_format(self, test_client: TestClient, sample_vehicle_data):
        """Test that datetime fields are in ISO 8601 format"""
        # Register a vehicle
        post_response = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        assert post_response.status_code == 201
        vehicle_id = post_response.json()["id"]
        
        response = test_client.get(f"/api/v1/vehicles/{vehicle_id}")
        assert response.status_code == 200
        
        vehicle_data = response.json()
        
        # Validate datetime format (ISO 8601)
        from datetime import datetime
        for field in ["created_at", "updated_at"]:
            assert field in vehicle_data
            # Should be able to parse as ISO 8601
            datetime.fromisoformat(vehicle_data[field].replace('Z', '+00:00'))
    
    def test_get_vehicle_empty_path_parameter(self, test_client: TestClient):
        """Test request with empty vehicle ID parameter"""
        response = test_client.get("/api/v1/vehicles/")
        
        # Should return 404 or 405 depending on routing implementation
        assert response.status_code in [404, 405]