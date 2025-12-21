from datetime import datetime, UTC
from remindermanagement.domain.model.aggregates.Event import Event
from remindermanagement.domain.model.commands.CreateEventCommand import CreateEventCommand
from remindermanagement.domain.model.commands.UpdateEventCommand import UpdateEventCommand
from remindermanagement.domain.model.commands.DeleteEventCommand import DeleteEventCommand
from remindermanagement.domain.repositories.EventRepository import EventRepository


class CommandServiceImpl:
    """
    Servicio de aplicación para Commands
    Orquesta la lógica de negocio para operaciones de escritura
    """

    def __init__(self, repository: EventRepository):
        self._repository = repository

    async def create_event(self, command: CreateEventCommand) -> Event:
        """
        Crear nuevo evento
        Valida y persiste el agregado
        """
        # Validación de negocio
        if command.event_date < datetime.now(UTC):
            raise ValueError("Cannot create event in the past")

        if not command.title.strip():
            raise ValueError("Title cannot be empty")

        # Crear agregado
        event = Event(
            user_id=command.user_id,
            title=command.title,
            description=command.description,
            event_date=command.event_date,
            status="pending"
        )

        # Persistir
        saved_event = await self._repository.save(event)

        # Aquí podrías emitir EventCreated si implementas event handlers

        return saved_event

    async def update_event(self, command: UpdateEventCommand) -> Event:
        """Actualizar evento existente"""
        event = await self._repository.find_by_id(command.event_id)

        if not event:
            raise ValueError(f"Event not found: {command.event_id}")

        # Aplicar cambios usando métodos del agregado
        if command.title or command.description:
            event.update_details(
                title=command.title,
                description=command.description
            )

        if command.event_date:
            event.reschedule(command.event_date)

        return await self._repository.save(event)

    async def delete_event(self, command: DeleteEventCommand) -> None:
        """Eliminar evento"""
        event = await self._repository.find_by_id(command.event_id)

        if not event:
            raise ValueError(f"Event not found: {command.event_id}")

        await self._repository.delete(event)

    async def complete_event(self, event_id: int) -> Event:
        """Marcar evento como completado"""
        event = await self._repository.find_by_id(event_id)

        if not event:
            raise ValueError(f"Event not found: {event_id}")

        event.mark_completed()
        return await self._repository.save(event)

    async def cancel_event(self, event_id: int) -> Event:
        """Cancelar evento"""
        event = await self._repository.find_by_id(event_id)

        if not event:
            raise ValueError(f"Event not found: {event_id}")

        event.cancel()
        return await self._repository.save(event)