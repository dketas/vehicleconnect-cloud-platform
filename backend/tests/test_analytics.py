from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analytics_kpis():
    """Test KPI endpoint returns valid data."""
    response = client.get("/api/analytics/kpis")
    assert response.status_code == 200
    data = response.json()
    assert "operational_kpis" in data
    assert "avg_latency_ms" in data["operational_kpis"]


def test_analytics_operational():
    """Test operational KPIs."""
    response = client.get("/api/analytics/kpis/operational")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["avg_latency_ms"], (int, float))
