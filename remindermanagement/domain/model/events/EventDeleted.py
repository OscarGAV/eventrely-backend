from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class EventDeleted:
    """Domain Event: Evento eliminado"""
    event_id: int
    occurred_at: datetime