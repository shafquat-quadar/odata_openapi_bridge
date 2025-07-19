from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from metadata_store import (
    list_services,
    add_service,
    toggle_service,
    delete_service,
    get_service,
    update_metadata,
)
from metadata_parser import fetch_metadata, parse_metadata_to_json


templates = Jinja2Templates(directory="ui/templates")


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def list_view(request: Request):
    services = list_services()
    return templates.TemplateResponse(
        "list.html", {"request": request, "services": services}
    )


@router.get("/add", response_class=HTMLResponse)
async def add_form(request: Request, error: str = ""):
    return templates.TemplateResponse("add.html", {"request": request, "error": error})


@router.post("/add")
async def add_service_post(request: Request, service_url: str = Form(...)):
    if not service_url.lower().startswith("https://"):
        error = "Service URL must use HTTPS"
        return templates.TemplateResponse(
            "add.html", {"request": request, "error": error, "service_url": service_url}
        )
    metadata_xml, version_hash = await fetch_metadata(service_url)
    metadata_json = parse_metadata_to_json(metadata_xml)
    add_service(service_url, metadata_json, version_hash)
    return RedirectResponse("/service", status_code=status.HTTP_302_FOUND)


@router.post("/{service_id}/toggle")
async def toggle_service_route(service_id: int):
    toggle_service(service_id)
    return RedirectResponse("/service", status_code=status.HTTP_302_FOUND)


@router.post("/{service_id}/delete")
async def delete_service_route(service_id: int):
    delete_service(service_id)
    return RedirectResponse("/service", status_code=status.HTTP_302_FOUND)


@router.post("/{service_id}/refresh")
async def refresh_service_route(service_id: int):
    svc = get_service(service_id)
    if svc:
        metadata_xml, version_hash = await fetch_metadata(svc["service_url"])
        metadata_json = parse_metadata_to_json(metadata_xml)
        update_metadata(service_id, metadata_json, version_hash)
    return RedirectResponse("/service", status_code=status.HTTP_302_FOUND)


@router.get("/{service_id}", response_class=HTMLResponse)
async def service_detail(request: Request, service_id: int):
    svc = get_service(service_id)
    if not svc:
        return RedirectResponse("/service", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "detail.html", {"request": request, "service": svc}
    )


def get_admin_app():
    from fastapi import FastAPI

    admin_app = FastAPI()
    admin_app.include_router(router)
    return admin_app
