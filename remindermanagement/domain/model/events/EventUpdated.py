from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class EventUpdated:
    """Domain Event: Evento actualizado"""
    event_id: int
    updated_fields: dict
    occurred_at: datetime