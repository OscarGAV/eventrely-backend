import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from remindermanagement.infrastructure.persistence.configuration.database_configuration import init_db, close_db
from remindermanagement.interface.api.rest.controllers.EventController import router as event_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Application lifecycle management.
    Handles startup and shutdown operations.
    The '_' argument prevents shadowing the outer 'app' variable 
    and signals that the variable is not used inside the function.
    """
    # Startup
    logger.info("Starting EventRELY API initialization...")

    try:
        await init_db()
        logger.info("Database connection established and initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    logger.info("EventRELY API is ready to accept requests.")

    yield

    # Shutdown
    logger.info("Shutting down EventRELY API...")
    await close_db()
    logger.info("Database connections closed.")
    logger.info("EventRELY API stopped successfully.")


# Create FastAPI application
app = FastAPI(
    title="EventRELY",
    description="A backend for event reminders",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware, # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(event_router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "service": "EventRELY",
        "status": "running",
        "architecture": "DDD + CQRS",
        "documentation": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "EventRELY"
    }


if __name__ == "__main__":
    logger.info("Starting server via uvicorn...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )