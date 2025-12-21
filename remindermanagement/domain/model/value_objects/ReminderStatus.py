from enum import Enum

class ReminderStatus(str, Enum):
    """Estados posibles de un recordatorio"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"