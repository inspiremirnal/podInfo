from app.api.health.health_router import set_app_ready
import logging

# Mock logger for testing
mock_logger = logging.getLogger()
mock_logger.info = lambda message, extra: None


def test_set_app_ready():
    """Test that set_app_ready sets is_app_ready to True"""
    is_app_ready = False

    # Act
    set_app_ready()

    # Assert
    assert is_app_ready is True
../../tests/test_health_router.py 