"""
Contract test for GET /api/v1/vehicles endpoint
Tests vehicle listing functionality according to OpenAPI specification

This test MUST FAIL initially - it's part of TDD approach.
Implementation will be created after all tests are written.
"""

import pytest
from fastapi.testclient import TestClient


class TestVehiclesGetContract:
    """Contract tests for vehicle listing endpoint"""
    
    def test_get_vehicles_empty_list(self, test_client: TestClient):
        """Test GET vehicles when no vehicles are registered"""
        response = test_client.get("/api/v1/vehicles")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert "vehicles" in response_data
        assert "total_count" in response_data
        assert "limit" in response_data
        assert "offset" in response_data
        
        assert response_data["vehicles"] == []
        assert response_data["total_count"] == 0
        assert response_data["limit"] == 20  # Default limit
        assert response_data["offset"] == 0   # Default offset
    
    def test_get_vehicles_with_data(self, test_client: TestClient, sample_vehicle_data):
        """Test GET vehicles when vehicles exist"""
        # First register a vehicle
        post_response = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        assert post_response.status_code == 201
        
        # Then list vehicles
        response = test_client.get("/api/v1/vehicles")
        assert response.status_code == 200
        
        response_data = response.json()
        assert len(response_data["vehicles"]) == 1
        assert response_data["total_count"] == 1
        
        vehicle = response_data["vehicles"][0]
        assert vehicle["vin"] == sample_vehicle_data["vin"]
        assert vehicle["model_year"] == sample_vehicle_data["model_year"]
    
    def test_get_vehicles_pagination_limit(self, test_client: TestClient):
        """Test GET vehicles with custom limit parameter"""
        response = test_client.get("/api/v1/vehicles?limit=5")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["limit"] == 5
        assert response_data["offset"] == 0
    
    def test_get_vehicles_pagination_offset(self, test_client: TestClient):
        """Test GET vehicles with custom offset parameter"""
        response = test_client.get("/api/v1/vehicles?offset=10")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["limit"] == 20  # Default
        assert response_data["offset"] == 10
    
    def test_get_vehicles_pagination_both(self, test_client: TestClient):
        """Test GET vehicles with both limit and offset parameters"""
        response = test_client.get("/api/v1/vehicles?limit=15&offset=5")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["limit"] == 15
        assert response_data["offset"] == 5
    
    def test_get_vehicles_invalid_limit_too_high(self, test_client: TestClient):
        """Test GET vehicles with limit exceeding maximum (100)"""
        response = test_client.get("/api/v1/vehicles?limit=150")
        
        assert response.status_code == 400
        
        error_data = response.json()
        assert "error" in error_data
        assert "limit" in error_data["message"].lower()
    
    def test_get_vehicles_invalid_limit_negative(self, test_client: TestClient):
        """Test GET vehicles with negative limit"""
        response = test_client.get("/api/v1/vehicles?limit=-1")
        
        assert response.status_code == 400
        
        error_data = response.json()
        assert "error" in error_data
    
    def test_get_vehicles_invalid_offset_negative(self, test_client: TestClient):
        """Test GET vehicles with negative offset"""
        response = test_client.get("/api/v1/vehicles?offset=-1")
        
        assert response.status_code == 400
        
        error_data = response.json()
        assert "error" in error_data
    
    def test_get_vehicles_invalid_limit_non_integer(self, test_client: TestClient):
        """Test GET vehicles with non-integer limit"""
        response = test_client.get("/api/v1/vehicles?limit=abc")
        
        assert response.status_code == 400
        
        error_data = response.json()
        assert "error" in error_data
    
    def test_get_vehicles_response_schema(self, test_client: TestClient, sample_vehicle_data):
        """Test that GET vehicles response matches expected schema"""
        # Register a vehicle first
        post_response = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        assert post_response.status_code == 201
        
        response = test_client.get("/api/v1/vehicles")
        assert response.status_code == 200
        
        response_data = response.json()
        
        # Validate top-level schema
        required_fields = ["vehicles", "total_count", "limit", "offset"]
        for field in required_fields:
            assert field in response_data
        
        # Validate vehicle object schema
        if response_data["vehicles"]:
            vehicle = response_data["vehicles"][0]
            vehicle_fields = ["id", "vin", "model_year", "created_at", "updated_at"]
            for field in vehicle_fields:
                assert field in vehicle