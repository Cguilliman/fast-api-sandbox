from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from base.routers import register_router
from config import settings


app = FastAPI(
    title=settings.PROJECT_NAME
)

app.mount(settings.STATIC_URL, StaticFiles(directory=settings.STATIC_PATH), name="static")
app.mount(settings.UPLOADS_URL, StaticFiles(directory=settings.UPLOADS_PATH), name="uploads")

# Init routers
register_router(app, "render.catalog.router")
register_router(app, "render.auth.router")
register_router(app, "rest.catalog.router")
