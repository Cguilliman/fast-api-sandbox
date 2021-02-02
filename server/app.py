from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from base.routers import register_router
from config import settings


app = FastAPI(
    title=settings.PROJECT_NAME
)
app.mount("/static", StaticFiles(directory="markup/static"), name="static")

# Init routers
register_router(app, "render.catalog.router")
