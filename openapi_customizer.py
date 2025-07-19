from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="OData OpenAPI Bridge",
        version="0.1.0",
        description="Bridge OData metadata into FastAPI endpoints.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
