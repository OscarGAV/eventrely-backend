from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class CreateEventRequest(BaseModel):
    """DTO for creating an event"""
    title: str = Field(..., min_length=1, max_length=200, description="Event title")
    event_date: datetime = Field(..., description="Event date and time (ISO 8601 format)")

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Pay rent",
                    "event_date": "2026-12-22T10:00:00"
                }
            ]
        }
    }


class UpdateEventRequest(BaseModel):
    """DTO for updating an event"""
    title: str | None = Field(None, min_length=1, max_length=200)
    event_date: datetime | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Pay rent - URGENT",
                    "event_date": "2026-12-23T10:00:00"
                }
            ]
        }
    }