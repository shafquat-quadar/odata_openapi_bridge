from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from metadata_store import init_db
from endpoint_generator import register_services
from openapi_customizer import custom_openapi
from admin.ui_app import get_admin_app


app = FastAPI(title="OData OpenAPI Bridge")


@app.on_event("startup")
async def startup_event():
    init_db()
    register_services(app)


app.mount("/service", get_admin_app(), name="service")
app.mount("/static", StaticFiles(directory="ui/static"), name="static")

app.openapi = lambda: custom_openapi(app)


@app.get("/", response_class=HTMLResponse)
async def root():
    return "<html><body><h1>OData OpenAPI Bridge</h1></body></html>"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
