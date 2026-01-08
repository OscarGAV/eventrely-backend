from datetime import datetime, date

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from remindermanagement.domain.model.aggregates.Event import Event


class EventRepositoryImpl:
    """
    Implementación concreta del repositorio de eventos
    Maneja toda la interacción con la base de datos
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, event: Event) -> Event:
        """Guardar o actualizar evento"""
        self._session.add(event)
        await self._session.commit()
        await self._session.refresh(event)
        return event

    async def find_by_id(self, event_id: int) -> Event | None:
        """Buscar evento por ID"""
        result = await self._session.execute(
            select(Event).where(Event.id == event_id)
        )
        return result.scalar_one_or_none()

    async def find_by_user(self, user_id: str) -> list[Event]:
        """Buscar todos los eventos de un usuario"""
        result = await self._session.execute(
            select(Event)
            .where(Event.user_id == user_id)
            .order_by(Event.event_date.desc())
        )
        return list(result.scalars().all())

    async def find_by_user_and_date(self, user_id: str, target_date: date) -> list[Event]:
        """Buscar eventos de un usuario en una fecha específica"""
        start_of_day = datetime.combine(target_date, datetime.min.time())
        end_of_day = datetime.combine(target_date, datetime.max.time())

        result = await self._session.execute(
            select(Event)
            .where(
                and_(
                    Event.user_id == user_id,
                    Event.event_date >= start_of_day,
                    Event.event_date <= end_of_day
                )
            )
            .order_by(Event.event_date)
        )
        return list(result.scalars().all())

    async def find_upcoming(self, user_id: str, from_date: datetime, limit: int) -> list[Event]:
        """Buscar eventos próximos de un usuario"""
        result = await self._session.execute(
            select(Event)
            .where(
                and_(
                    Event.user_id == user_id,
                    Event.event_date >= from_date,
                    Event.status == "pending"
                )
            )
            .order_by(Event.event_date)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def delete(self, event: Event) -> None:
        """Eliminar evento"""
        await self._session.delete(event)
        await self._session.commit()

    # =========================================================================
    # ADMIN METHODS - Para que admins puedan ver eventos de todos los usuarios
    # =========================================================================

    async def find_all(self) -> list[Event]:
        """
        Buscar TODOS los eventos (de todos los usuarios)
        SOLO PARA ADMINS
        """
        result = await self._session.execute(
            select(Event).order_by(Event.event_date.desc())
        )
        return list(result.scalars().all())

    async def find_by_date(self, target_date: date) -> list[Event]:
        """
        Buscar TODOS los eventos en una fecha específica (de todos los usuarios)
        SOLO PARA ADMINS
        """
        start_of_day = datetime.combine(target_date, datetime.min.time())
        end_of_day = datetime.combine(target_date, datetime.max.time())

        result = await self._session.execute(
            select(Event)
            .where(
                and_(
                    Event.event_date >= start_of_day,
                    Event.event_date <= end_of_day
                )
            )
            .order_by(Event.event_date)
        )
        return list(result.scalars().all())

    async def find_all_upcoming(self, from_date: datetime, limit: int) -> list[Event]:
        """
        Buscar TODOS los eventos próximos (de todos los usuarios)
        SOLO PARA ADMINS
        """
        result = await self._session.execute(
            select(Event)
            .where(
                and_(
                    Event.event_date >= from_date,
                    Event.status == "pending"
                )
            )
            .order_by(Event.event_date)
            .limit(limit)
        )
        return list(result.scalars().all())