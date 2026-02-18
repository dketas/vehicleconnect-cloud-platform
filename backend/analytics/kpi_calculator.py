"""
VehicleConnect KPI Calculator
Turns raw API events into business metrics.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Any

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text


class KPICalculator:
    """
    Core analytics engine. Loads events from DB and computes KPIs.
    """

    def __init__(self, database_url: str | None = None):
        """
        Initialize with database connection.
        """
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "postgresql://vc_user:vc_password@postgres:5432/vehicleconnect",
        )
        self.engine = create_engine(self.database_url)

    def get_events_dataframe(self, hours: int = 24) -> pd.DataFrame:
        """
        Fetch recent events from database as pandas DataFrame.
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        query = text(
            """
            SELECT
                id, timestamp, endpoint, method, status_code,
                response_time_ms, client_id, success, error_message
            FROM api_events
            WHERE timestamp > :cutoff_time
            ORDER BY timestamp DESC
            """
        )

        df = pd.read_sql(query, self.engine, params={"cutoff_time": cutoff_time})
        print(f"📊 Loaded {len(df):,} events from past {hours}h")
        return df

    def calculate_operational_kpis(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate operational KPIs from events DataFrame.
        """
        if df.empty:
            return {
                "avg_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
                "p99_latency_ms": 0.0,
                "error_rate_percent": 0.0,
                "total_requests": 0,
                "requests_per_minute": 0.0,
                "availability_percent": 100.0,
            }

        total_requests = len(df)
        failed_requests = len(df[~df["success"]])
        error_rate = (failed_requests / total_requests * 100) if total_requests > 0 else 0.0

        latencies = df["response_time_ms"].dropna()
        avg_latency = latencies.mean()
        p95_latency = latencies.quantile(0.95)
        p99_latency = latencies.quantile(0.99)

        time_span_minutes = (df["timestamp"].max() - df["timestamp"].min()).total_seconds() / 60
        req_per_min = total_requests / time_span_minutes if time_span_minutes > 0 else 0.0

        return {
            "avg_latency_ms": round(float(avg_latency), 2),
            "p95_latency_ms": round(float(p95_latency), 2),
            "p99_latency_ms": round(float(p99_latency), 2),
            "error_rate_percent": round(float(error_rate), 2),
            "total_requests": int(total_requests),
            "requests_per_minute": round(float(req_per_min), 2),
            "availability_percent": round(float(100 - error_rate), 2),
        }

    def generate_kpi_report(self, hours: int = 24) -> Dict[str, Any]:
        """
        Generate complete KPI report for dashboard.
        """
        df = self.get_events_dataframe(hours)

        return {
            "report_timestamp": datetime.utcnow().isoformat(),
            "analysis_period_hours": hours,
            "total_events_analyzed": len(df),
            "operational_kpis": self.calculate_operational_kpis(df),
        }
