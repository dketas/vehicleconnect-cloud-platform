from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dashboard_html():
    r = client.get("/dashboard/")
    assert r.status_code == 200
    assert b"VehicleConnect Cloud Dashboard" in r.content

def test_static_css():
    r = client.get("/static/css/style.css")
    assert r.status_code == 200
