import unittest
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
import app.api.health.health_router
import logging

logger = logging.getLogger(__name__)


class TestHealthCheck(unittest.TestCase):
    def setUp(self):
        # Setup test app
        self.app = FastAPI()
        self.app.include_router(app.api.health.health_router.router)
        self.client = TestClient(self.app)
        app.api.health.health_router.is_app_ready = False

    def tearDown(self):
        app.api.health.health_router.is_app_ready = False

    def test_set_app_ready(self):
        """Test that set_app_ready sets is_app_ready to True"""
        # Reset the module state before testing
        app.api.health.is_app_ready = False

        # Verify initial state
        print(f"Before: {app.api.health.health_router.is_app_ready}")
        assert app.api.health.health_router.is_app_ready is False

        # Call the function
        app.api.health.health_router.set_app_ready()

        # Verify the state was changed
        print(f"After: {app.api.health.health_router.is_app_ready}")
        assert app.api.health.health_router.is_app_ready is True


    def test_health_check_not_ready(self):
        """Test health check when app is not ready"""
        app.api.health.health_router.is_app_ready = False

        # Make the request
        response = self.client.get("/local")

        # Verify response
        assert response.status_code == 503
        assert response.json() == {"status": "unhealthy", "reason": "application is starting up"}

    def test_health_check_ready(self):
        """Test health check when app is ready"""
        app.api.health.health_router.set_app_ready()

        response = self.client.get("/local")

        # Verify response
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

