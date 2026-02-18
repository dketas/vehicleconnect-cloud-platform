from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from datetime import datetime
import time

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from .database import init_db, get_db, APIEvent
from .schemas import EventCreate, EventResponse, StatusResponse


app = FastAPI(
    title="VehicleConnect Cloud API",
    description="Backend for VehicleConnect Cloud Platform (connected vehicle monitoring)",
    version="1.0.0",
)


# For now we allow all origins (frontend will be on same origin anyway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


START_TIME = time.time()


# Prometheus Metrics (global counters and histograms)
REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status']
)


REQUEST_LATENCY = Histogram(
    'api_request_duration_seconds',
    'API request latency in seconds',
    ['method', 'endpoint']
)


ERROR_COUNT = Counter(
    'api_errors_total',
    'Total API errors',
    ['endpoint']
)


@app.on_event("startup")
def on_startup():
    """
    Run when the application starts.
    Here we ensure the database tables exist.
    """
    init_db()
    print("✅ Database initialized")


@app.get("/", response_model=StatusResponse)
def root():
    """
    Simple health check.
    Useful for load balancers and uptime checks.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "uptime_seconds": time.time() - START_TIME,
    }


@app.get("/api/status", response_model=StatusResponse)
def get_status():
    """
    More explicit API status endpoint.
    """
    return {
        "status": "operational",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "uptime_seconds": time.time() - START_TIME,
    }


@app.post("/api/events", response_model=EventResponse, status_code=201)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Store a new API event in the database.
    Updates Prometheus metrics automatically.
    """
    try:
        # Update Prometheus counters BEFORE saving to DB
        REQUEST_COUNT.labels(
            method=event.method,
            endpoint=event.endpoint,
            status=event.status_code
        ).inc()
        
        # Track latency in seconds (Prometheus standard)
        REQUEST_LATENCY.labels(
            method=event.method,
            endpoint=event.endpoint
        ).observe(event.response_time_ms / 1000.0)
        
        if not event.success:
            ERROR_COUNT.labels(endpoint=event.endpoint).inc()

        # Save to database
        db_event = APIEvent(**event.model_dump())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/events", response_model=list[EventResponse])
def list_events(
    limit: int = 100,
    skip: int = 0,
    db: Session = Depends(get_db),
):
    """
    Return the most recent events from the database.

    - limit: max number of records to return
    - skip: number of records to skip (for pagination)
    """
    events = (
        db.query(APIEvent)
        .order_by(APIEvent.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return events


@app.get("/metrics")
def prometheus_metrics():
    """
    Prometheus metrics endpoint.
    Prometheus scrapes this every 15 seconds.
    """
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    """
    Simple plain-text health endpoint (often used by Kubernetes).
    """
    return "ok"

# Analytics routes
from .analytics_routes import router as analytics_router
app.include_router(analytics_router)
