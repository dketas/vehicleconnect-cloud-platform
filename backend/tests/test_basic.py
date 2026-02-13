from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_health():
    """Test the root health endpoint returns 200 OK"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_status_endpoint():
    """Test the /api/status endpoint"""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"


def test_create_event_and_list():
    """Test creating an event and listing events"""
    # Create an event
    event_data = {
        "endpoint": "/api/test",
        "method": "GET",
        "status_code": 200,
        "response_time_ms": 42.5,
        "client_id": "test_client",
        "success": True,
    }
    
    response = client.post("/api/events", json=event_data)
    assert response.status_code == 201
    created = response.json()
    assert created["endpoint"] == "/api/test"
    assert created["method"] == "GET"
    
    # List events
    response = client.get("/api/events?limit=10")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    assert len(events) > 0
