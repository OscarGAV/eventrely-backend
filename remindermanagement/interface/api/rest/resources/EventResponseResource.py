from pydantic import BaseModel, Field
from datetime import datetime


class EventResponse(BaseModel):
    """DTO for event output"""
    id: int = Field(..., description="Unique event ID")
    title: str = Field(..., description="Event title")
    event_date: datetime = Field(..., description="Event date and time")
    status: str = Field(..., description="Status: pending, completed, cancelled, expired")
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Pay rent",
                    "event_date": "2026-12-22T10:00:00",
                    "status": "pending",
                    "created_at": "2026-12-21T15:30:00",
                    "updated_at": "2026-12-21T15:30:00"
                }
            ]
        }
    }


class EventListResponse(BaseModel):
    """DTO for list of events"""
    events: list[EventResponse]
    total: int = Field(..., description="Total number of events")