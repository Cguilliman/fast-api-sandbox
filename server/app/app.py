from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME
)
app.mount("/static", StaticFiles(directory="markup/static"), name="static")

# Init routers
from render.catalog import router
app.include_router(router)
