import os
import unittest
from unittest.mock import patch
from app.services.system_info import SystemInfoService


class TestSystemInfoService(unittest.TestCase):
    def setUp(self):
        self.service = SystemInfoService()

    @patch.dict(os.environ, {}, clear=True)
    def test_get_system_info_with_unset_env_vars(self):
        expected_result = {
            "pod": {
                "pod_name": "N/A",
                "pod_ip": "N/A",
                "pod_namespace": "N/A",
                "pod_service_account": "N/A",
                "pod_uid": "N/A"
            },
            "node": {
                "node_name": "N/A",
                "node_ip": "N/A",
                "host_ip": "N/A"
            },
            "container": {
                "container_name": "N/A",
                "container_image": "N/A",
                "container_cpu_request": "N/A",
                "container_memory_request": "N/A"
            },
            "system": {
                "hostname": "test_hostname",
                "platform": "test_platform",
                "python_version": "test_python_version"
            }
        }
        with patch("socket.gethostname", return_value="test_hostname"), \
                patch("platform.platform", return_value="test_platform"), \
                patch("platform.python_version", return_value="test_python_version"):
            result = self.service.get_system_info()
            self.assertEqual(result, expected_result)

    @patch.dict(os.environ, {
        "HOSTNAME": "test-pod",
        "POD_IP": "10.1.2.3",
        "POD_NAMESPACE": "test-namespace",
        "POD_SERVICE_ACCOUNT": "test-service-account",
        "POD_UID": "1234567890",
        "NODE_NAME": "test-node",
        "NODE_IP": "192.168.1.1",
        "HOST_IP": "192.168.1.2",
        "CONTAINER_NAME": "test-container",
        "CONTAINER_IMAGE": "test-image:latest",
        "CONTAINER_CPU_REQUEST": "100m",
        "CONTAINER_MEMORY_REQUEST": "512Mi"
    })
    def test_get_system_info_with_env_vars(self):
        expected_result = {
            "pod": {
                "pod_name": "test-pod",
                "pod_ip": "10.1.2.3",
                "pod_namespace": "test-namespace",
                "pod_service_account": "test-service-account",
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
                "container_cpu_request": "100m",
                "container_memory_request": "512Mi"
            },
            "system": {
                "hostname": "test-hostname",
                "platform": "test-platform",
                "python_version": "test-python-version"
            }
        }
        with patch("socket.gethostname", return_value="test-hostname"), \
                patch("platform.platform", return_value="test-platform"), \
                patch("platform.python_version", return_value="test-python-version"):
            result = self.service.get_system_info()
            self.assertEqual(result, expected_result)
