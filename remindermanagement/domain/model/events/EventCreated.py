from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class EventCreated:
    """Domain Event: Evento creado"""
    event_id: int
    user_id: str
    title: str
    event_date: datetime
    occurred_at: datetime