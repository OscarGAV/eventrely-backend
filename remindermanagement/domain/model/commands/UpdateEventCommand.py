from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class UpdateEventCommand:
    """Command: Actualizar evento existente"""
    event_id: int
    title: str | None = None
    event_date: datetime | None = None