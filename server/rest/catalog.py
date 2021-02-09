from fastapi.routing import APIRouter
from pydantic import BaseModel
import base64


router = APIRouter(prefix="/api/v1")


class PostItem(BaseModel):
    title: str
    description: str
    preview: str


@router.post("/post/create/")
async def create_post(item: PostItem):
    print(item)
    # TODO: validate preview
    return {"status": "OK"}
