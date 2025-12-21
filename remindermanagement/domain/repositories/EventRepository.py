from typing import Protocol
from datetime import datetime, date
from remindermanagement.domain.model.aggregates.Event import Event


class EventRepository(Protocol):
    """
    Interface del repositorio de eventos
    Define el contrato que debe cumplir la implementación
    """

    async def save(self, event: Event) -> Event:
        """Persistir o actualizar un evento"""
        ...

    async def find_by_id(self, event_id: int) -> Event | None:
        """Buscar evento por ID"""
        ...

    async def find_by_user(self, user_id: str) -> list[Event]:
        """Buscar todos los eventos de un usuario"""
        ...

    async def find_by_user_and_date(self, user_id: str, target_date: date) -> list[Event]:
        """Buscar eventos de un usuario en una fecha específica"""
        ...

    async def find_upcoming(self, user_id: str, from_date: datetime, limit: int) -> list[Event]:
        """Buscar eventos próximos de un usuario"""
        ...

    async def delete(self, event: Event) -> None:
        """Eliminar un evento"""
        ...