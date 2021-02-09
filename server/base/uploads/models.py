from pydantic import BaseModel


class Image(BaseModel):
    filename: str
    image: str
