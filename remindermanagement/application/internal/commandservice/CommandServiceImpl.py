from datetime import datetime, timezone
from remindermanagement.domain.model.aggregates.Event import Event
from remindermanagement.domain.model.commands.CreateEventCommand import CreateEventCommand
from remindermanagement.domain.model.commands.UpdateEventCommand import UpdateEventCommand
from remindermanagement.domain.model.commands.DeleteEventCommand import DeleteEventCommand
from remindermanagement.domain.model.value_objects.ReminderStatus import ReminderStatus
from remindermanagement.domain.repositories.EventRepository import EventRepository


def ensure_utc(dt: datetime) -> datetime:
    """Ensure datetime is timezone-aware (UTC)"""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def utc_now() -> datetime:
    """Get current UTC time"""
    return datetime.now(timezone.utc)


class CommandServiceImpl:
    """
    Servicio de aplicación para Commands
    Orquesta la lógica de negocio para operaciones de escritura
    """

    def __init__(self, repository: EventRepository):
        self._repository = repository

    """
    Crear un nuevo evento
    """
    async def create_event(self, command: CreateEventCommand) -> Event:
        # Asegurar que la fecha del evento es timezone-aware (UTC)
        event_date = ensure_utc(command.event_date)
        current_time = utc_now()

        # Validación de negocio
        if event_date < current_time:
            raise ValueError("Cannot create event in the past")

        if not command.title.strip():
            raise ValueError("Title cannot be empty")

        # Crear agregado
        event = Event(
            user_id=command.user_id,
            title=command.title,
            event_date=event_date,
            status=ReminderStatus.PENDING,
        )

        saved_event = await self._repository.save(event)
        return saved_event

    """
    Actualizar un evento existente
    """
    async def update_event(self, command: UpdateEventCommand) -> Event:
        # Validar que el evento existe
        event = await self._repository.find_by_id(command.event_id)

        if not event:
            raise ValueError(f"Event not found: {command.event_id}")

        # Aplicar cambios usando métodos del agregado
        if command.title:
            event.update_details(
                title=command.title
            )

        if command.event_date:
            # Ensure timezone-aware
            event_date = ensure_utc(command.event_date)
            event.reschedule(event_date)

        return await self._repository.save(event)

    """
    Eliminar evento
    """
    async def delete_event(self, command: DeleteEventCommand) -> None:
        # Validar que el evento existe
        event = await self._repository.find_by_id(command.event_id)

        if not event:
            raise ValueError(f"Event not found: {command.event_id}")

        await self._repository.delete(event)

    """
    Asignar evento como completado
    """
    async def complete_event(self, event_id: int) -> Event:
        # Validar que el evento existe
        event = await self._repository.find_by_id(event_id)

        if not event:
            raise ValueError(f"Event not found: {event_id}")

        event.mark_completed()
        return await self._repository.save(event)

    """
    Cancelar evento
    """
    async def cancel_event(self, event_id: int) -> Event:
        # Validar que el evento existe
        event = await self._repository.find_by_id(event_id)

        if not event:
            raise ValueError(f"Event not found: {event_id}")

        event.cancel()
        return await self._repository.save(event)