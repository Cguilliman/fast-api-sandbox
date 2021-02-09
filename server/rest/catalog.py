from fastapi.routing import APIRouter
from pydantic import BaseModel

from base.uploads.models import Image
from base.uploads.usecases import save_base64_image


router = APIRouter(prefix="/api/v1")


class PostItem(BaseModel):
    title: str
    description: str
    preview: Image


@router.post("/post/create/")
async def create_post(item: PostItem):
    print(await save_base64_image(item.preview))
    return {"status": "OK"}
