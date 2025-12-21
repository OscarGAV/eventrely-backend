from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class CreateEventCommand:
    """
    Command: Crear nuevo evento
    Inmutable para garantizar integridad
    """
    user_id: str
    title: str
    event_date: datetime
    description: str | None = None