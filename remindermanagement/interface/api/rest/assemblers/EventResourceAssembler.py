from datetime import datetime, date
from remindermanagement.domain.model.commands.CreateEventCommand import CreateEventCommand
from remindermanagement.domain.model.commands.UpdateEventCommand import UpdateEventCommand
from remindermanagement.domain.model.commands.DeleteEventCommand import DeleteEventCommand
from remindermanagement.domain.model.queries.GetEventByIdQuery import GetEventByIdQuery
from remindermanagement.domain.model.queries.GetEventsByDateQuery import GetEventsByDateQuery
from remindermanagement.domain.model.queries.GetUpcomingEventsQuery import GetUpcomingEventsQuery
from remindermanagement.domain.model.aggregates.Event import Event
from remindermanagement.interface.api.rest.resources.EventRequestResource import CreateEventRequest, UpdateEventRequest
from remindermanagement.interface.api.rest.resources.EventResponseResource import EventResponse, EventListResponse


class EventResourceAssembler:
    """
    Assembler para transformar entre capa de presentación y dominio
    Transformaciones: Resource ↔ Command/Query
    """

    # =========================================================================
    # Resource → Command
    # =========================================================================

    @staticmethod
    def to_create_command(resource: CreateEventRequest) -> CreateEventCommand:
        """Convertir CreateEventRequest → CreateEventCommand"""
        return CreateEventCommand(
            user_id=resource.user_id,
            title=resource.title,
            event_date=resource.event_date,
        )

    @staticmethod
    def to_update_command(event_id: int, resource: UpdateEventRequest) -> UpdateEventCommand:
        """Convertir UpdateEventRequest → UpdateEventCommand"""
        return UpdateEventCommand(
            event_id=event_id,
            title=resource.title,
            event_date=resource.event_date
        )

    @staticmethod
    def to_delete_command(event_id: int) -> DeleteEventCommand:
        """Crear DeleteEventCommand"""
        return DeleteEventCommand(event_id=event_id)

    # =========================================================================
    # Params → Query
    # =========================================================================

    @staticmethod
    def to_get_by_id_query(event_id: int) -> GetEventByIdQuery:
        """Crear GetEventByIdQuery"""
        return GetEventByIdQuery(event_id=event_id)

    @staticmethod
    def to_get_by_date_query(user_id: str, target_date: date) -> GetEventsByDateQuery:
        """Crear GetEventsByDateQuery"""
        return GetEventsByDateQuery(
            user_id=user_id,
            target_date=target_date
        )

    @staticmethod
    def to_get_upcoming_query(user_id: str, from_date: datetime, limit: int) -> GetUpcomingEventsQuery:
        """Crear GetUpcomingEventsQuery"""
        return GetUpcomingEventsQuery(
            user_id=user_id,
            from_date=from_date,
            limit=limit
        )

    # =========================================================================
    # Aggregate → Response
    # =========================================================================

    @staticmethod
    def to_response(event: Event) -> EventResponse:
        """Convertir Event → EventResponse"""
        return EventResponse(
            id=event.id,
            user_id=event.user_id,
            title=event.title,
            event_date=event.event_date,
            status=event.status,
            created_at=event.created_at,
            updated_at=event.updated_at
        )

    @staticmethod
    def to_list_response(events: list[Event]) -> EventListResponse:
        """Convertir lista de Event → EventListResponse"""
        return EventListResponse(
            events=[EventResourceAssembler.to_response(e) for e in events],
            total=len(events)
        )