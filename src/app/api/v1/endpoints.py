from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from src.app.services.system_info import SystemInfoService
import logging

router = APIRouter()
system_info_service = SystemInfoService()

# Setup Jinja2 templates
BASE_PATH = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))
logger = logging.getLogger(__name__)


# Endpoint to get system information including Kubernetes metadata and container information
@router.get("/whoami", response_class=HTMLResponse)
async def whoami(request: Request):
    """Returns information about the Pod and the node it is running on"""
    try:
        system_info = system_info_service.get_system_info()
        print("Debug - System Info:", system_info)  # Debug print
        context = {
            "request": request,  # Required by Jinja2
            "info": {
                "pod": {
                    "pod_name": system_info.get("pod", {}).get("pod_name", "N/A"),
                    "pod_ip": system_info.get("pod", {}).get("pod_ip", "N/A"),
                    "pod_namespace": system_info.get("pod", {}).get("pod_namespace", "N/A"),
                    "pod_service_account": system_info.get("pod", {}).get("pod_service_account", "N/A"),
                    "pod_uid": system_info.get("pod", {}).get("pod_uid", "N/A")
                },
                "node": {
                    "node_name": system_info.get("node", {}).get("node_name", "N/A"),
                    "node_ip": system_info.get("node", {}).get("node_ip", "N/A"),
                    "host_ip": system_info.get("node", {}).get("host_ip", "N/A")
                },
                "container": {
                    "container_name": system_info.get("container", {}).get("container_name", "N/A"),
                    "container_image": system_info.get("container", {}).get("container_image", "N/A"),
                    "container_cpu_request": system_info.get("container", {}).get("container_cpu_request", "N/A"),
                    "container_memory_request": system_info.get("container", {}).get("container_memory_request", "N/A")
                },
                "system": {
                    "hostname": system_info.get("system", {}).get("hostname", "N/A"),
                    "platform": system_info.get("system", {}).get("platform", "N/A"),
                    "python_version": system_info.get("system", {}).get("python_version", "N/A")
                }
            }
        }
        logger.debug("System info collected successfully",
                     extra={"event": "system_info_collected"})
        return templates.TemplateResponse("whoami.html", context)
    except Exception as e:
        logger.error("Failed to collect system info",
                     extra={
                         "event": "system_info_failed",
                         "error": str(e)
                     })
        raise
