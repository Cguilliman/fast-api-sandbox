import base64
from .models import Image
from .images.config import ImageConfig
from .images.service import ImageService
from config import settings


async def save_base64_image(image: Image, config: ImageConfig):
    header, _data = image.image.split(';base64,')
    image_data = base64.b64decode(_data)
    file_path = await ImageService.save(
        image_data=image_data,
        filename=image.filename,
        uploads_path=settings.UPLOADS_PATH,
        config=config,
    )
    return file_path
