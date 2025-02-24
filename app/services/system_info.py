import os
import platform
import socket
import logging

logger = logging.getLogger(__name__)


class SystemInfoService:
    def get_system_info(self):
        """Gather system information including Kubernetes metadata"""
        # Pod information from Kubernetes Downward API
        pod_info = {
            "pod_name": os.getenv("HOSTNAME", "N/A"),  # K8s sets HOSTNAME to pod name
            "pod_ip": os.getenv("POD_IP", "N/A"),
            "pod_namespace": os.getenv("POD_NAMESPACE", "N/A"),
            "pod_service_account": os.getenv("POD_SERVICE_ACCOUNT", "N/A"),
            "pod_uid": os.getenv("POD_UID", "N/A")
        }

        # Node information
        node_info = {
            "node_name": os.getenv("NODE_NAME", "N/A"),
            "node_ip": os.getenv("NODE_IP", "N/A"),
            "host_ip": os.getenv("HOST_IP", "N/A")
        }

        # Container information
        container_info = {
            "container_name": os.getenv("CONTAINER_NAME", "N/A"),
            "container_image": os.getenv("CONTAINER_IMAGE", "N/A"),
            "container_cpu_request": os.getenv("CONTAINER_CPU_REQUEST", "N/A"),
            "container_memory_request": os.getenv("CONTAINER_MEMORY_REQUEST", "N/A")
        }

        # System information
        sys_info = {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "python_version": platform.python_version()
        }
        logger.debug("System info collected successfully",
                     extra={"event": "system_info_collected"})
        return {
            "pod": pod_info,
            "node": node_info,
            "container": container_info,
            "system": sys_info
        }
