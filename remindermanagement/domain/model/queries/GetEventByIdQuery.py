from dataclasses import dataclass

@dataclass(frozen=True)
class GetEventByIdQuery:
    """Query: Obtener evento por ID"""
    event_id: int