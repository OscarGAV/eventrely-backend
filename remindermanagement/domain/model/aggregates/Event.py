from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.persistence.configuration.database_configuration import Base


class Event(Base):
    """
    Aggregate Root: Evento de recordatorio
    Combina el modelo de dominio con la persistencia ORM
    """
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(nullable=False, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    event_date: Mapped[datetime] = mapped_column(nullable=False, index=True)
    status: Mapped[str] = mapped_column(default="pending")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # =========================================================================
    # DOMAIN LOGIC - Métodos que protegen invariantes del negocio
    # =========================================================================

    def reschedule(self, new_date: datetime) -> None:
        """
        Reprogramar evento con validación de negocio
        Regla: No se puede programar un evento en el pasado
        """
        if new_date < datetime.utcnow():
            raise ValueError("Cannot schedule event in the past")

        self.event_date = new_date
        self.updated_at = datetime.utcnow()

    def update_details(self, title: str | None = None, description: str | None = None) -> None:
        """Actualizar título y/o descripción"""
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            self.title = title

        if description is not None:
            self.description = description

        self.updated_at = datetime.utcnow()

    def mark_completed(self) -> None:
        """
        Marcar como completado
        Regla: Solo eventos pendientes pueden completarse
        """
        if self.status != "pending":
            raise ValueError(f"Cannot complete event with status: {self.status}")

        self.status = "completed"
        self.updated_at = datetime.utcnow()

    def cancel(self) -> None:
        """
        Cancelar evento
        Regla: No se pueden cancelar eventos ya completados
        """
        if self.status == "completed":
            raise ValueError("Cannot cancel a completed event")

        self.status = "cancelled"
        self.updated_at = datetime.utcnow()

    def mark_expired(self) -> None:
        """Marcar como expirado (proceso automático)"""
        if self.status == "pending" and self.event_date < datetime.utcnow():
            self.status = "expired"
            self.updated_at = datetime.utcnow()

    def is_upcoming(self) -> bool:
        """Verifica si el evento es futuro y está pendiente"""
        return self.status == "pending" and self.event_date >= datetime.utcnow()

    def to_dict(self) -> dict:
        """Serialización para respuestas API"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "event_date": self.event_date.isoformat(),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }