from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Global flag to track application startup status
is_app_ready: bool = False


def set_app_ready():
    """Called when application has fully started"""
    global is_app_ready
    is_app_ready = True
    logger.info("Application marked as ready", extra={"event": "app_ready"})


@router.get("/local")
async def health_check() -> JSONResponse:
    """
    Health check endpoint that returns:
    - 200 if application is healthy
    - 503 if application is starting up or unhealthy
    """
    if not is_app_ready:
        logger.error("Health check failed - application not ready",
                     extra={"event": "health_check_failed"})
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "reason": "application is starting up"}
        )
    logger.debug("Health check passed", extra={"event": "health_check_passed"})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy"}
    )
