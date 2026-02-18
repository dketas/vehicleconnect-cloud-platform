from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

# Database URL: user:password@host:port/dbname
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://vc_user:vc_password@localhost:5432/vehicleconnect"
)

# SQLAlchemy engine: manages connections to DB
engine = create_engine(DATABASE_URL, echo=False)

# Session factory: used in each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


class APIEvent(Base):
    """
    Stores one API call from a 'vehicle' or client.
    Each row is one event.
    """
    __tablename__ = "api_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    endpoint = Column(String, index=True)          # e.g. "/api/vehicle/status"
    method = Column(String)                        # GET/POST/PUT...
    status_code = Column(Integer)                  # HTTP status, e.g. 200, 500
    response_time_ms = Column(Float)               # latency in milliseconds
    client_id = Column(String, index=True)         # e.g. "vehicle_00123"
    error_message = Column(String, nullable=True)  # error text if any
    success = Column(Boolean, default=True)        # True if request succeeded
class KPISnapshot(Base):
    """
    Stores calculated KPIs over time for trend analysis.
    """
    __tablename__ = "kpi_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    kpi_name = Column(String, index=True)           # e.g. "avg_latency_ms"
    kpi_value = Column(Float)                       # The calculated value
    kpi_category = Column(String)                   # operational, security, delivery


def init_db():
    """
    Create tables in the database based on the models above.
    Called at app startup.
    """
    Base.metadata.create_all(bind=engine)


# Dependency for FastAPI: get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
