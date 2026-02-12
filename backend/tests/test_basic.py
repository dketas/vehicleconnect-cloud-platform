from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_health():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "operational")


def test_status_endpoint():
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"


def test_create_event_and_list():
    event = {
        "endpoint": "/api/test",
        "method": "GET",
        "status_code": 200,
        "response_time_ms": 12.3,
        "client_id": "test_client",
        "error_message": None,
        "success": True
    }
    create_res = client.post("/api/events", json=event)
    assert create_res.status_code == 201
    created = create_res.json()
    assert created["endpoint"] == "/api/test"

    list_res = client.get("/api/events")
    assert list_res.status_code == 200
    events = list_res.json()
    assert any(e["endpoint"] == "/api/test" for e in events)
