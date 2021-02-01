from fastapi.requests import Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.jinja import templates


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
