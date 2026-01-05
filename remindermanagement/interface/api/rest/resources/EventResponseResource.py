from pydantic import BaseModel, Field
from datetime import datetime


class EventResponse(BaseModel):
    """DTO de salida para eventos"""
    id: int = Field(..., description="ID único del evento")
    user_id: str = Field(..., description="ID del usuario propietario")
    title: str = Field(..., description="Título del evento")
    event_date: datetime = Field(..., description="Fecha y hora del evento")
    status: str = Field(..., description="Estado: pending, completed, cancelled, expired")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "user_id": "user_123",
                    "title": "Pagar alquiler",
                    "event_date": "2025-12-22T10:00:00",
                    "status": "pending",
                    "created_at": "2025-12-21T15:30:00",
                    "updated_at": "2025-12-21T15:30:00"
                }
            ]
        }
    }


class EventListResponse(BaseModel):
    """DTO de salida para lista de eventos"""
    events: list[EventResponse]
    total: int = Field(..., description="Total de eventos")