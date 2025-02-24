from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from src.app.api.v1 import endpoints
from src.app.api.health import health_router
from src.app.api.health.health_router import set_app_ready
from src.app.core.logging_config import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup logging first thing
    setup_logging()

    # Startup logic
    logger.info("Application startup in progress", extra={"event": "startup_initiated"})
    set_app_ready()
    logger.info("Application startup completed", extra={"event": "startup_completed"})

    yield

    # Shutdown logic
    logger.info("Application shutdown initiated", extra={"event": "shutdown_initiated"})


app = FastAPI(lifespan=lifespan, title="System Info Microservice")

# Include routers
app.include_router(endpoints.router, prefix="/v1")
app.include_router(health_router.router, prefix="/health")
