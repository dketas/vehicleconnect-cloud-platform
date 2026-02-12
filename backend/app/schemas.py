from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventCreate(BaseModel):
    """
    Shape of data sent by client when creating an event.
    """
    endpoint: str
    method: str
    status_code: int
    response_time_ms: float
    client_id: str
    error_message: Optional[str] = None
    success: bool = True


class EventResponse(BaseModel):
    """
    Shape of event data returned to the client.
    """
    id: int
    timestamp: datetime
    endpoint: str
    method: str
    status_code: int
    response_time_ms: float
    client_id: str
    success: bool

    class Config:
        from_attributes = True  # allow reading from SQLAlchemy model


class StatusResponse(BaseModel):
    """
    Shape of the health/status response.
    """
    status: str
    timestamp: datetime
    version: str
    uptime_seconds: float
