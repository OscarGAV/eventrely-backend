from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class EventDate:
    """Value Object: Fecha del evento con validaciones"""
    value: datetime

    def __post_init__(self):
        if not isinstance(self.value, datetime):
            raise ValueError("Event date must be a datetime object")

    def is_in_past(self) -> bool:
        """Verifica si la fecha está en el pasado"""
        return self.value < datetime.utcnow()

    def is_upcoming(self) -> bool:
        """Verifica si la fecha es futura"""
        return self.value >= datetime.utcnow()