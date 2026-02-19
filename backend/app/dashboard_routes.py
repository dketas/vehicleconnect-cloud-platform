import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DASHBOARD_DIR = os.path.join(BACKEND_ROOT, "dashboard")


@router.get("/", response_class=HTMLResponse)
def dashboard_home():
    html_path = os.path.join(DASHBOARD_DIR, "templates", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())
