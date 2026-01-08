# =============================================================================
# ACTUALIZACIÓN: EventController.py
# Agregar protección JWT a los endpoints de eventos
# =============================================================================

from datetime import datetime, date, UTC
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infrastructure.persistence.configuration.database_configuration import get_db_session
from remindermanagement.application.internal.commandservice.CommandServiceImpl import CommandServiceImpl
from remindermanagement.application.internal.queryservice.QueryServiceImpl import QueryServiceImpl
from remindermanagement.infrastructure.persistence.repositories.EventRepositoryImpl import EventRepositoryImpl

from remindermanagement.interface.api.rest.resources.EventRequestResource import CreateEventRequest, UpdateEventRequest
from remindermanagement.interface.api.rest.resources.EventResponseResource import EventResponse, EventListResponse
from remindermanagement.interface.api.rest.assemblers.EventResourceAssembler import EventResourceAssembler

# NUEVO: Import JWT dependency
from iam.infrastructure.tokenservice.jwt.BearerTokenService import (
    get_current_active_user,
    get_current_general_user
)
from iam.domain.model.aggregates.User import User

router = APIRouter(prefix="/api/v1/events", tags=["Events"])


# =============================================================================
# COMMANDS (Write Operations) - PROTEGIDOS CON JWT
# =============================================================================

@router.post(
    "/",
    response_model=EventResponse,
    status_code=201,
    summary="Create new event",
    description="Create a new reminder event. Requires authentication.",
    responses={
        201: {"description": "Event created successfully"},
        400: {"description": "Invalid request or business rule violation"},
        401: {"description": "Authentication required"},
        500: {"description": "Internal server error"}
    }
)
async def create_event(
        request: CreateEventRequest,
        current_user: User = Depends(get_current_general_user),  # SOLO GENERAL USERS
        db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new reminder event

    **Requires authentication (JWT token) - GENERAL USERS ONLY**

    - **title**: Event title (required, max 200 chars)
    - **event_date**: Event date and time in ISO 8601 format
    - **description**: Optional event description (max 1000 chars)

    Users can only create events for themselves.
    Admin users cannot create events.
    """
    try:
        repository = EventRepositoryImpl(db)
        service = CommandServiceImpl(repository)

        # IMPORTANTE: Sobrescribir user_id con el del token JWT
        # Esto previene que usuarios creen eventos para otros usuarios
        request.user_id = str(current_user.id)  # Usar el user_id del JWT

        command = EventResourceAssembler.to_create_command(request)
        event = await service.create_event(command)

        return EventResourceAssembler.to_response(event)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.put(
    "/{event_id}",
    response_model=EventResponse,
    summary="Update event",
    description="Update an existing event. User can only update their own events.",
    responses={
        200: {"description": "Event updated successfully"},
        400: {"description": "Invalid request or business rule violation"},
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized to update this event"},
        404: {"description": "Event not found"},
        500: {"description": "Internal server error"}
    }
)
async def update_event(
        event_id: int = Path(..., ge=1, description="Event ID to update"),
        request: UpdateEventRequest = ...,
        current_user: User = Depends(get_current_general_user),  # SOLO GENERAL USERS
        db: AsyncSession = Depends(get_db_session)
):
    """
    Update an existing event

    **Requires authentication (JWT token) - GENERAL USERS ONLY**

    Users can only update their own events.
    Admin users cannot update events.
    """
    try:
        repository = EventRepositoryImpl(db)
        service = CommandServiceImpl(repository)

        # NUEVO: Verificar que el evento pertenece al usuario
        existing_event = await repository.find_by_id(event_id)
        if not existing_event:
            raise HTTPException(status_code=404, detail=f"Event not found: {event_id}")

        if existing_event.user_id != str(current_user.id):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to update this event"
            )

        command = EventResourceAssembler.to_update_command(event_id, request)
        event = await service.update_event(command)

        return EventResourceAssembler.to_response(event)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.delete(
    "/{event_id}",
    status_code=204,
    summary="Delete event",
    description="Permanently delete an event. User can only delete their own events.",
    responses={
        204: {"description": "Event deleted successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized to delete this event"},
        404: {"description": "Event not found"},
        500: {"description": "Internal server error"}
    }
)
async def delete_event(
        event_id: int = Path(..., ge=1, description="Event ID to delete"),
        current_user: User = Depends(get_current_general_user),  # SOLO GENERAL USERS
        db: AsyncSession = Depends(get_db_session)
):
    """
    Delete an event permanently

    **Requires authentication (JWT token) - GENERAL USERS ONLY**

    Users can only delete their own events.
    Admin users cannot delete events.
    """
    try:
        repository = EventRepositoryImpl(db)
        service = CommandServiceImpl(repository)

        # NUEVO: Verificar que el evento pertenece al usuario
        existing_event = await repository.find_by_id(event_id)
        if not existing_event:
            raise HTTPException(status_code=404, detail=f"Event not found: {event_id}")

        if existing_event.user_id != str(current_user.id):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this event"
            )

        command = EventResourceAssembler.to_delete_command(event_id)
        await service.delete_event(command)

        return None

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post(
    "/{event_id}/complete",
    response_model=EventResponse,
    summary="Mark event as completed",
    description="Change event status to completed",
    responses={
        200: {"description": "Event marked as completed"},
        400: {"description": "Business rule violation"},
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized"},
        404: {"description": "Event not found"}
    }
)
async def complete_event(
        event_id: int = Path(..., ge=1, description="Event ID to complete"),
        current_user: User = Depends(get_current_general_user),  # SOLO GENERAL USERS
        db: AsyncSession = Depends(get_db_session)
):
    """Mark an event as completed (requires authentication)"""
    try:
        repository = EventRepositoryImpl(db)
        service = CommandServiceImpl(repository)

        # Verificar ownership
        existing_event = await repository.find_by_id(event_id)
        if not existing_event:
            raise HTTPException(status_code=404, detail=f"Event not found: {event_id}")

        if existing_event.user_id != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not authorized")

        event = await service.complete_event(event_id)
        return EventResourceAssembler.to_response(event)

    except HTTPException:
        raise
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post(
    "/{event_id}/cancel",
    response_model=EventResponse,
    summary="Cancel event",
    description="Change event status to cancelled",
    responses={
        200: {"description": "Event cancelled"},
        400: {"description": "Business rule violation"},
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized"},
        404: {"description": "Event not found"}
    }
)
async def cancel_event(
        event_id: int = Path(..., ge=1, description="Event ID to cancel"),
        current_user: User = Depends(get_current_general_user),  # SOLO GENERAL USERS
        db: AsyncSession = Depends(get_db_session)
):
    """Cancel an event (requires authentication)"""
    try:
        repository = EventRepositoryImpl(db)
        service = CommandServiceImpl(repository)

        # Verificar ownership
        existing_event = await repository.find_by_id(event_id)
        if not existing_event:
            raise HTTPException(status_code=404, detail=f"Event not found: {event_id}")

        if existing_event.user_id != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not authorized")

        event = await service.cancel_event(event_id)
        return EventResourceAssembler.to_response(event)

    except HTTPException:
        raise
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


# =============================================================================
# QUERIES (Read Operations) - PROTEGIDOS CON JWT
# =============================================================================

@router.get(
    "/",
    response_model=EventListResponse,
    summary="Get all events",
    description="General users see only their events. Admins see all events from all users.",
    responses={
        200: {"description": "Events retrieved successfully"},
        401: {"description": "Authentication required"}
    }
)
async def get_all_events(
        current_user: User = Depends(get_current_active_user),  # Ambos roles permitidos
        db: AsyncSession = Depends(get_db_session)
):
    """
    Get events based on user role

    **Requires authentication (JWT token)**

    - **General users**: Returns only their own events
    - **Admin users**: Returns events from ALL users
    """
    repository = EventRepositoryImpl(db)
    service = QueryServiceImpl(repository)

    # Admin can see all events, general users only their own
    if current_user.is_admin():
        # Get ALL events from ALL users
        events = await repository.find_all()  # Necesitamos agregar este método
    else:
        # Get only current user's events
        events = await service.get_user_events(str(current_user.id))

    return EventResourceAssembler.to_list_response(events)


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get event by ID",
    description="General users can only view their own events. Admins can view any event.",
    responses={
        200: {"description": "Event found"},
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized to view this event"},
        404: {"description": "Event not found"}
    }
)
async def get_event(
        event_id: int = Path(..., ge=1, description="Event ID to retrieve"),
        current_user: User = Depends(get_current_active_user),  # Ambos roles permitidos
        db: AsyncSession = Depends(get_db_session)
):
    """
    Get a specific event by ID

    **Requires authentication (JWT token)**

    - **General users**: Can only view their own events
    - **Admin users**: Can view any event
    """
    repository = EventRepositoryImpl(db)
    service = QueryServiceImpl(repository)

    query = EventResourceAssembler.to_get_by_id_query(event_id)
    event = await service.get_event_by_id(query)

    if not event:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

    # Admin can view all events, general users only their own
    if not current_user.is_admin() and event.user_id != str(current_user.id):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this event"
        )

    return EventResourceAssembler.to_response(event)


@router.get(
    "/date/{target_date}",
    response_model=EventListResponse,
    summary="Get events by date",
    description="General users see only their events. Admins see all events from all users on that date.",
    responses={
        200: {"description": "Events retrieved successfully"},
        401: {"description": "Authentication required"}
    }
)
async def get_events_by_date(
        target_date: date = Path(..., description="Target date (YYYY-MM-DD)"),
        current_user: User = Depends(get_current_active_user),  # Ambos roles permitidos
        db: AsyncSession = Depends(get_db_session)
):
    """
    Get all events on a specific date

    **Requires authentication (JWT token)**

    - **General users**: Returns only their own events on that date
    - **Admin users**: Returns all events from all users on that date
    """
    repository = EventRepositoryImpl(db)
    service = QueryServiceImpl(repository)

    if current_user.is_admin():
        # Admin: Get all events on this date from all users
        events = await repository.find_by_date(target_date)  # Necesitamos agregar este método
    else:
        # General user: Get only their events on this date
        query = EventResourceAssembler.to_get_by_date_query(str(current_user.id), target_date)
        events = await service.get_events_by_date(query)

    return EventResourceAssembler.to_list_response(events)


@router.get(
    "/upcoming",
    response_model=EventListResponse,
    summary="Get upcoming events",
    description="General users see only their upcoming events. Admins see all upcoming events from all users.",
    responses={
        200: {"description": "Upcoming events retrieved successfully"},
        401: {"description": "Authentication required"}
    }
)
async def get_upcoming_events(
        limit: int = Query(50, ge=1, le=100, description="Maximum number of events to return"),
        current_user: User = Depends(get_current_active_user),  # Ambos roles permitidos
        db: AsyncSession = Depends(get_db_session)
):
    """
    Get upcoming events

    **Requires authentication (JWT token)**

    - **General users**: Returns only their upcoming pending events
    - **Admin users**: Returns all upcoming pending events from all users

    Returns only pending events with future dates, ordered by event_date
    """
    repository = EventRepositoryImpl(db)
    service = QueryServiceImpl(repository)

    if current_user.is_admin():
        # Admin: Get all upcoming events from all users
        events = await repository.find_all_upcoming(datetime.now(UTC), limit)  # Necesitamos agregar
    else:
        # General user: Get only their upcoming events
        query = EventResourceAssembler.to_get_upcoming_query(
            user_id=str(current_user.id),
            from_date=datetime.now(UTC),
            limit=limit
        )
        events = await service.get_upcoming_events(query)

    return EventResourceAssembler.to_list_response(events)