from datetime import datetime, date, UTC
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from remindermanagement.infrastructure.persistence.configuration.database_configuration import get_db_session
from remindermanagement.application.internal.commandservice.CommandServiceImpl import CommandServiceImpl
from remindermanagement.application.internal.queryservice.QueryServiceImpl import QueryServiceImpl
from remindermanagement.infrastructure.persistence.repositories.EventRepositoryImpl import EventRepositoryImpl

from remindermanagement.interface.api.rest.resources.EventRequestResource import CreateEventRequest, UpdateEventRequest
from remindermanagement.interface.api.rest.resources.EventResponseResource import EventResponse, EventListResponse
from remindermanagement.interface.api.rest.assemblers.EventResourceAssembler import EventResourceAssembler

router = APIRouter(prefix="/api/v1/events", tags=["Events"])


# =============================================================================
# COMMANDS (Write Operations)
# =============================================================================

@router.post(
    "/",
    response_model=EventResponse,
    status_code=201,
    summary="Create new event",
    description="Create a new reminder event. The event date must be in the future.",
    responses={
        201: {"description": "Event created successfully"},
        400: {"description": "Invalid request or business rule violation"},
        500: {"description": "Internal server error"}
    }
)
async def create_event(
        request: CreateEventRequest,
        db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new reminder event

    - **user_id**: User identifier
    - **title**: Event title (required, max 200 chars)
    - **event_date**: Event date and time in ISO 8601 format
    - **description**: Optional event description (max 1000 chars)
    """
    try:
        repository = EventRepositoryImpl(db)
        service = CommandServiceImpl(repository)

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
    description="Update an existing event's details",
    responses={
        200: {"description": "Event updated successfully"},
        400: {"description": "Invalid request or business rule violation"},
        404: {"description": "Event not found"},
        500: {"description": "Internal server error"}
    }
)
async def update_event(
        event_id: int = Path(..., ge=1, description="Event ID to update"),
        request: UpdateEventRequest = ...,
        db: AsyncSession = Depends(get_db_session)
):
    """
    Update an existing event

    You can update one or more fields:
    - **title**: New event title
    - **description**: New description
    - **event_date**: New date/time for the event
    """
    try:
        repository = EventRepositoryImpl(db)
        service = CommandServiceImpl(repository)

        command = EventResourceAssembler.to_update_command(event_id, request)
        event = await service.update_event(command)

        return EventResourceAssembler.to_response(event)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.delete(
    "/{event_id}",
    status_code=204,
    summary="Delete event",
    description="Permanently delete an event",
    responses={
        204: {"description": "Event deleted successfully"},
        404: {"description": "Event not found"},
        500: {"description": "Internal server error"}
    }
)
async def delete_event(
        event_id: int = Path(..., ge=1, description="Event ID to delete"),
        db: AsyncSession = Depends(get_db_session)
):
    """Delete an event permanently"""
    try:
        repository = EventRepositoryImpl(db)
        service = CommandServiceImpl(repository)

        command = EventResourceAssembler.to_delete_command(event_id)
        await service.delete_event(command)

        return None

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
        404: {"description": "Event not found"}
    }
)
async def complete_event(
        event_id: int = Path(..., ge=1, description="Event ID to complete"),
        db: AsyncSession = Depends(get_db_session)
):
    """Mark an event as completed"""
    try:
        repository = EventRepositoryImpl(db)
        service = CommandServiceImpl(repository)

        event = await service.complete_event(event_id)
        return EventResourceAssembler.to_response(event)

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
        404: {"description": "Event not found"}
    }
)
async def cancel_event(
        event_id: int = Path(..., ge=1, description="Event ID to cancel"),
        db: AsyncSession = Depends(get_db_session)
):
    """Cancel an event"""
    try:
        repository = EventRepositoryImpl(db)
        service = CommandServiceImpl(repository)

        event = await service.cancel_event(event_id)
        return EventResourceAssembler.to_response(event)

    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


# =============================================================================
# QUERIES (Read Operations)
# =============================================================================

@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get event by ID",
    description="Retrieve a single event by its ID",
    responses={
        200: {"description": "Event found"},
        404: {"description": "Event not found"}
    }
)
async def get_event(
        event_id: int = Path(..., ge=1, description="Event ID to retrieve"),
        db: AsyncSession = Depends(get_db_session)
):
    """Get a specific event by ID"""
    repository = EventRepositoryImpl(db)
    service = QueryServiceImpl(repository)

    query = EventResourceAssembler.to_get_by_id_query(event_id)
    event = await service.get_event_by_id(query)

    if not event:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

    return EventResourceAssembler.to_response(event)


@router.get(
    "/user/{user_id}",
    response_model=EventListResponse,
    summary="Get all user events",
    description="Retrieve all events for a specific user",
    responses={
        200: {"description": "Events retrieved successfully"}
    }
)
async def get_user_events(
        user_id: str = Path(..., min_length=1, description="User ID"),
        db: AsyncSession = Depends(get_db_session)
):
    """Get all events for a user"""
    repository = EventRepositoryImpl(db)
    service = QueryServiceImpl(repository)

    events = await service.get_user_events(user_id)
    return EventResourceAssembler.to_list_response(events)


@router.get(
    "/user/{user_id}/date/{target_date}",
    response_model=EventListResponse,
    summary="Get events by date",
    description="Retrieve all events for a user on a specific date",
    responses={
        200: {"description": "Events retrieved successfully"}
    }
)
async def get_events_by_date(
        user_id: str = Path(..., min_length=1, description="User ID"),
        target_date: date = Path(..., description="Target date (YYYY-MM-DD)"),
        db: AsyncSession = Depends(get_db_session)
):
    """Get all events for a user on a specific date"""
    repository = EventRepositoryImpl(db)
    service = QueryServiceImpl(repository)

    query = EventResourceAssembler.to_get_by_date_query(user_id, target_date)
    events = await service.get_events_by_date(query)

    return EventResourceAssembler.to_list_response(events)


@router.get(
    "/user/{user_id}/upcoming",
    response_model=EventListResponse,
    summary="Get upcoming events",
    description="Retrieve upcoming pending events for a user",
    responses={
        200: {"description": "Upcoming events retrieved successfully"}
    }
)
async def get_upcoming_events(
        user_id: str = Path(..., min_length=1, description="User ID"),
        limit: int = Query(50, ge=1, le=100, description="Maximum number of events to return"),
        db: AsyncSession = Depends(get_db_session)
):
    """
    Get upcoming events for a user

    Returns only pending events with future dates, ordered by event_date
    """
    repository = EventRepositoryImpl(db)
    service = QueryServiceImpl(repository)

    query = EventResourceAssembler.to_get_upcoming_query(
        user_id=user_id,
        from_date=datetime.now(UTC),
        limit=limit
    )
    events = await service.get_upcoming_events(query)

    return EventResourceAssembler.to_list_response(events)