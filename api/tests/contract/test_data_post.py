"""
Contract test for POST /api/v1/sessions/{sessionId}/data endpoint
Tests system data submission functionality according to OpenAPI specification

This test MUST FAIL initially - it's part of TDD approach.
Implementation will be created after all tests are written.
"""

import pytest
from fastapi.testclient import TestClient


class TestDataPostContract:
    """Contract tests for system data submission endpoint"""
    
    def test_post_data_success(self, test_client: TestClient, sample_vehicle_data, sample_session_data, sample_system_data):
        """Test successful system data submission"""
        # Setup: Register vehicle and create session
        vehicle_response = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        assert vehicle_response.status_code == 201
        vehicle_id = vehicle_response.json()["id"]
        
        session_response = test_client.post(f"/api/v1/vehicles/{vehicle_id}/sessions", json=sample_session_data)
        assert session_response.status_code == 201
        session_id = session_response.json()["id"]
        
        # Submit system data
        data_payload = {"data_points": sample_system_data}
        response = test_client.post(f"/api/v1/sessions/{session_id}/data", json=data_payload)
        
        assert response.status_code == 201
        
        response_data = response.json()
        assert "added_count" in response_data
        assert "data_points" in response_data
        assert response_data["added_count"] == len(sample_system_data)
        assert len(response_data["data_points"]) == len(sample_system_data)
        
        # Validate first data point structure
        data_point = response_data["data_points"][0]
        assert "id" in data_point
        assert "session_id" in data_point
        assert data_point["session_id"] == session_id
        assert data_point["parameter_name"] == sample_system_data[0]["parameter_name"]
        assert data_point["converted_value"] == sample_system_data[0]["converted_value"]
    
    def test_post_data_session_not_found(self, test_client: TestClient, sample_system_data):
        """Test data submission for non-existent session returns 404"""
        non_existent_id = "550e8400-e29b-41d4-a716-446655440000"
        data_payload = {"data_points": sample_system_data}
        
        response = test_client.post(f"/api/v1/sessions/{non_existent_id}/data", json=data_payload)
        assert response.status_code == 404
        
        error_data = response.json()
        assert "error" in error_data
        assert "session not found" in error_data["message"].lower()
    
    def test_post_data_invalid_session_id(self, test_client: TestClient, sample_system_data):
        """Test data submission with invalid session ID format"""
        invalid_id = "not-a-valid-uuid"
        data_payload = {"data_points": sample_system_data}
        
        response = test_client.post(f"/api/v1/sessions/{invalid_id}/data", json=data_payload)
        assert response.status_code == 400
        
        error_data = response.json()
        assert "error" in error_data
    
    def test_post_data_empty_data_points(self, test_client: TestClient, sample_vehicle_data, sample_session_data):
        """Test data submission with empty data points array"""
        # Setup session
        vehicle_response = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        vehicle_id = vehicle_response.json()["id"]
        session_response = test_client.post(f"/api/v1/vehicles/{vehicle_id}/sessions", json=sample_session_data)
        session_id = session_response.json()["id"]
        
        data_payload = {"data_points": []}
        response = test_client.post(f"/api/v1/sessions/{session_id}/data", json=data_payload)
        
        assert response.status_code == 400
        error_data = response.json()
        assert "error" in error_data
        assert "data_points" in error_data["message"].lower()
    
    def test_post_data_too_many_points(self, test_client: TestClient, sample_vehicle_data, sample_session_data):
        """Test data submission with too many data points (>1000)"""
        # Setup session
        vehicle_response = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        vehicle_id = vehicle_response.json()["id"]
        session_response = test_client.post(f"/api/v1/vehicles/{vehicle_id}/sessions", json=sample_session_data)
        session_id = session_response.json()["id"]
        
        # Create oversized data payload
        large_data = []
        for i in range(1001):
            large_data.append({
                "timestamp": f"2025-09-12T10:{i//60:02d}:{i%60:02d}Z",
                "parameter_name": "SPEED",
                "parameter_id": "01 0D",
                "raw_value": str(i % 100),
                "converted_value": float(i % 100),
                "unit": "km/h",
                "is_error_code": False
            })
        
        data_payload = {"data_points": large_data}
        response = test_client.post(f"/api/v1/sessions/{session_id}/data", json=data_payload)
        
        assert response.status_code == 400
        error_data = response.json()
        assert "error" in error_data
        assert "1000" in error_data["message"]
    
    def test_post_data_missing_required_fields(self, test_client: TestClient, sample_vehicle_data, sample_session_data):
        """Test data submission with missing required fields"""
        # Setup session
        vehicle_response = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        vehicle_id = vehicle_response.json()["id"]
        session_response = test_client.post(f"/api/v1/vehicles/{vehicle_id}/sessions", json=sample_session_data)
        session_id = session_response.json()["id"]
        
        incomplete_data = [{
            "timestamp": "2025-09-12T10:00:00Z",
            "parameter_name": "SPEED"
            # Missing required fields: parameter_id, raw_value
        }]
        
        data_payload = {"data_points": incomplete_data}
        response = test_client.post(f"/api/v1/sessions/{session_id}/data", json=data_payload)
        
        assert response.status_code == 400
        error_data = response.json()
        assert "error" in error_data
    
    def test_post_data_invalid_timestamp_format(self, test_client: TestClient, sample_vehicle_data, sample_session_data):
        """Test data submission with invalid timestamp format"""
        # Setup session
        vehicle_response = test_client.post("/api/v1/vehicles", json=sample_vehicle_data)
        vehicle_id = vehicle_response.json()["id"]
        session_response = test_client.post(f"/api/v1/vehicles/{vehicle_id}/sessions", json=sample_session_data)
        session_id = session_response.json()["id"]
        
        invalid_data = [{
            "timestamp": "invalid-timestamp",
            "parameter_name": "SPEED",
            "parameter_id": "01 0D",
            "raw_value": "50",
            "converted_value": 50.0,
            "unit": "km/h",
            "is_error_code": False
        }]
        
        data_payload = {"data_points": invalid_data}
        response = test_client.post(f"/api/v1/sessions/{session_id}/data", json=data_payload)
        
        assert response.status_code == 400
        error_data = response.json()
        assert "error" in error_data
    
    def test_post_data_session_not_active(self, test_client: TestClient, sample_vehicle_data, sample_session_data, sample_system_data):
        """Test data submission to completed/failed session"""
        # This test would require first completing a session
        # For now, we'll focus on the basic contract validation
        # Implementation will handle session state validation
        pass