from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime

from remindermanagement.domain.model.value_objects.ReminderStatus import ReminderStatus
from shared.infrastructure.persistence.configuration.database_configuration import Base


def utc_now() -> datetime:
    """Get current UTC time as timezone-aware datetime"""
    return datetime.now(timezone.utc)


class Event(Base):
    """
    Aggregate Root: Evento de recordatorio
    Combina el modelo de dominio con la persistencia ORM
    """
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(nullable=False, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(default=ReminderStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # =========================================================================
    # DOMAIN LOGIC - Métodos que protegen invariantes del negocio
    # =========================================================================

    def reschedule(self, new_date: datetime) -> None:
        """
        Reprogramar evento con validación de negocio
        Regla: No se puede programar un evento en el pasado
        """
        # Ensure new_date is timezone-aware
        if new_date.tzinfo is None:
            new_date = new_date.replace(tzinfo=timezone.utc)

        current_time = utc_now()

        if new_date < current_time:
            raise ValueError("Cannot schedule event in the past")

        self.event_date = new_date
        self.updated_at = current_time

    def update_details(self, title: str | None = None) -> None:
        """Actualizar título del evento"""
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            self.title = title

        self.updated_at = utc_now()

    def mark_completed(self) -> None:
        """
        Marcar como completado
        Regla: Solo eventos pendientes pueden completarse
        """
        if self.status != ReminderStatus.PENDING:
            raise ValueError(f"Cannot complete event with status: {self.status}")

        self.status = ReminderStatus.COMPLETED
        self.updated_at = utc_now()

    def cancel(self) -> None:
        """
        Cancelar evento
        Regla: No se pueden cancelar eventos ya completados
        """
        if self.status != ReminderStatus.PENDING:
            raise ValueError("Cannot cancel a completed event")

        self.status = ReminderStatus.CANCELLED
        self.updated_at = utc_now()

    def is_upcoming(self) -> bool:
        """Verifica si el evento es futuro y está pendiente"""
        event_date = self.event_date
        if event_date.tzinfo is None:
            event_date = event_date.replace(tzinfo=timezone.utc)

        return self.status == ReminderStatus.PENDING and event_date >= utc_now()

    def to_dict(self) -> dict:
        """Serialización para respuestas API"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "event_date": self.event_date.isoformat(),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }