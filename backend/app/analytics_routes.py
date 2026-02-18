from fastapi import APIRouter, HTTPException
import os

from analytics.kpi_calculator import KPICalculator

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://vc_user:vc_password@postgres:5432/vehicleconnect",
)


@router.get("/kpis")
def get_full_kpis(hours: int = 24):
    """Full KPI report."""
    try:
        calc = KPICalculator(DATABASE_URL)
        return calc.generate_kpi_report(hours=hours)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")


@router.get("/kpis/operational")
def get_operational_kpis(hours: int = 24):
    """Operational KPIs only."""
    try:
        calc = KPICalculator(DATABASE_URL)
        df = calc.get_events_dataframe(hours=hours)
        return calc.calculate_operational_kpis(df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")
