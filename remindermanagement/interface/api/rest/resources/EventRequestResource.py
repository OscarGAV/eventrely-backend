from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class CreateEventRequest(BaseModel):
    """DTO de entrada para crear evento"""
    user_id: str = Field(..., min_length=1, description="ID del usuario")
    title: str = Field(..., min_length=1, max_length=200, description="Título del evento")
    event_date: datetime = Field(..., description="Fecha y hora del evento (ISO 8601)")

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
                    "user_id": "user_123",
                    "title": "Pagar alquiler",
                    "event_date": "2025-12-22T10:00:00",
                }
            ]
        }
    }


class UpdateEventRequest(BaseModel):
    """DTO de entrada para actualizar evento"""
    title: str | None = Field(None, min_length=1, max_length=200)
    event_date: datetime | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Pagar alquiler - URGENTE",
                    "event_date": "2025-12-23T10:00:00"
                }
            ]
        }
    }
