from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class GetUpcomingEventsQuery:
    """Query: Obtener eventos próximos de un usuario"""
    user_id: str
    from_date: datetime
    limit: int = 50
