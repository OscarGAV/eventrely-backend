from dataclasses import dataclass

@dataclass(frozen=True)
class DeleteEventCommand:
    """Command: Eliminar evento"""
    event_id: int