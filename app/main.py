from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI(title="Time Tracker")

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Routers
from app.routers.health import router as health_router  # noqa: E402
from app.database import engine, Base
from app import models

app.include_router(health_router)


@app.get("/", include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse(
        "base.html",
        {"request": request, "title": "Dashboard"},
    )


@app.on_event("startup")
def on_startup():
    # Create tables on first run
    Base.metadata.create_all(bind=engine)

