from dataclasses import dataclass

@dataclass(frozen=True)
class EventId:
    """Value Object: Identificador del evento"""
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Event ID must be positive")