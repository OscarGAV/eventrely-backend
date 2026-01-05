from enum import Enum

class ReminderStatus(str, Enum):
    """Estados posibles de un recordatorio"""
    PENDING = "pending"
    CANCELLED = "cancelled"
    COMPLETED = "completed"