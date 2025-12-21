from remindermanagement.domain.model.aggregates.Event import Event
from remindermanagement.domain.model.queries.GetEventByIdQuery import GetEventByIdQuery
from remindermanagement.domain.model.queries.GetEventsByDateQuery import GetEventsByDateQuery
from remindermanagement.domain.model.queries.GetUpcomingEventsQuery import GetUpcomingEventsQuery
from remindermanagement.domain.repositories.EventRepository import EventRepository


class QueryServiceImpl:
    """
    Servicio de aplicación para Queries
    Orquesta la lógica de consultas (solo lectura)
    """

    def __init__(self, repository: EventRepository):
        self._repository = repository

    async def get_event_by_id(self, query: GetEventByIdQuery) -> Event | None:
        """Obtener evento por ID"""
        return await self._repository.find_by_id(query.event_id)

    async def get_events_by_date(self, query: GetEventsByDateQuery) -> list[Event]:
        """Obtener eventos de una fecha específica"""
        return await self._repository.find_by_user_and_date(
            query.user_id,
            query.target_date
        )

    async def get_upcoming_events(self, query: GetUpcomingEventsQuery) -> list[Event]:
        """Obtener eventos próximos"""
        return await self._repository.find_upcoming(
            query.user_id,
            query.from_date,
            query.limit
        )

    async def get_user_events(self, user_id: str) -> list[Event]:
        """Obtener todos los eventos de un usuario"""
        return await self._repository.find_by_user(user_id)