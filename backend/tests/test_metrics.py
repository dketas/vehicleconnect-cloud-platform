from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_metrics_endpoint():
    """Test that /metrics returns Prometheus format"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "api_requests_total" in response.text
    assert "text/plain" in response.headers["content-type"]


def test_metrics_after_event():
    """Test that metrics update after posting event"""
    # Post an event
    event_data = {
        "endpoint": "/test",
        "method": "GET",
        "status_code": 200,
        "response_time_ms": 50.0,
        "client_id": "test_vehicle",
        "success": True,
    }
    
    response = client.post("/api/events", json=event_data)
    assert response.status_code == 201
    
    # Check metrics updated
    metrics_response = client.get("/metrics")
    assert "api_requests_total" in metrics_response.text
