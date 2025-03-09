import unittest
from unittest import mock
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.api.v1.endpoints import router, system_info_service
from app.services.system_info import SystemInfoService


class TestWhoamiEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(router)

    @patch.object(SystemInfoService, 'get_system_info', side_effect=Exception('Service temporarily unavailable'))
    def test_whoami_endpoint_handles_service_unavailability(self, mock_get_system_info):
        response = self.client.get('/whoami')
        assert response.status_code == 500
        assert response.json() == {
            'detail': 'Internal Server Error'
        }

    @patch.object(SystemInfoService, 'get_system_info', return_value={
        "pod": {
            "pod_name": "test-pod",
            "pod_ip": "10.1.2.3",
            "pod_namespace": "default",
            "pod_service_account": "default",
            "pod_uid": "1234567890"
        },
        "node": {
            "node_name": "test-node",
            "node_ip": "192.168.1.1",
            "host_ip": "192.168.1.2"
        },
        "container": {
            "container_name": "test-container",
            "container_image": "test-image:latest",
            "container_cpu_request": "500m",
            "container_memory_request": "256Mi"
        },
        "system": {
            "hostname": "test-hostname",
            "platform": "Linux",
            "python_version": "3.9.18"
        }
    })
    def test_whoami_endpoint_returns_valid_response_when_system_info_service_is_available(self, mock_get_system_info):
        client = TestClient(router)
        response = client.get('/whoami')
        assert response.status_code == 200
        assert response.template.name == "whoami.html"
        assert response.context["info"] == {
            "pod": {
                "pod_name": "test-pod",
                "pod_ip": "10.1.2.3",
                "pod_namespace": "default",
                "pod_service_account": "default",
                "pod_uid": "1234567890"
            },
            "node": {
                "node_name": "test-node",
                "node_ip": "192.168.1.1",
                "host_ip": "192.168.1.2"
            },
            "container": {
                "container_name": "test-container",
                "container_image": "test-image:latest",
                "container_cpu_request": "500m",
                "container_memory_request": "256Mi"
            },
            "system": {
                "hostname": "test-hostname",
                "platform": "Linux",
                "python_version": "3.9.18"
            }
        }
