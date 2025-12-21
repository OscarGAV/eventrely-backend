from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class GetEventsByDateQuery:
    """Query: Obtener eventos de un usuario en una fecha específica"""
    user_id: str
    target_date: date
