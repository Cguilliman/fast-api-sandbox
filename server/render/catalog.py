from fastapi.requests import Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from jinja import templates
from shared.humanize_filters.parser import parse


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/catalog/", response_class=HTMLResponse)
@router.get("/catalog/filters/{filters}/", response_class=HTMLResponse)
async def catalog(request: Request, filters: str = None):
    print(parse(filters))
    # TODO: Filter products
    return templates.TemplateResponse("catalog.html", {"request": request, "filters": filters})


@router.get("catalog/{product_slug}/detail", response_class=HTMLResponse)
async def product_detail(request: Request, product_slug: str):
    # TODO: Get product by slug
    return templates.TemplateResponse("product_detail.html", {"request": request})
