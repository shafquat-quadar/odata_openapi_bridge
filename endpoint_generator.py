from fastapi import FastAPI
from typing import Dict
from metadata_store import get_service, list_services


def register_services(app: FastAPI):
    """Register basic endpoints for each active service."""
    services = list_services()
    for svc in services:
        if not svc["active"]:
            continue
        prefix = f"/odata/{svc['id']}"

        @app.get(prefix)
        async def service_root(service_id=svc["id"]):
            service = get_service(service_id)
            return {
                "service": service["service_url"],
                "metadata_available": bool(service["metadata_json"]),
            }
