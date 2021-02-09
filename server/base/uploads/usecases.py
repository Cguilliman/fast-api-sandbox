import base64
import os

from config import settings
from .base import save_file
from .models import Image
from .images.optimizer import optimize
from .images.config import ImageConfig
from ..utils import get_random_string


def get_file_folder(base_folder, filename):
    name, _ = filename.rsplit(".", 1)
    path = f"{base_folder}{name}/"
    while True:
        if not os.path.exists(path):
            break
        name = f"{name}_{get_random_string(3)}"
        path = f"{base_folder}{name}/"
    return path


async def image_process(filename, image_data, config: ImageConfig):
    base_folder = (
        f"{settings.UPLOADS_PATH}{config.folder}/"
        if config.folder else settings.UPLOADS_PATH
    )
    folder = get_file_folder(base_folder, filename=filename)
    # Save instance image file
    instance_file_path = await save_file(folder, filename, image_data)
    if config.is_optimizer:
        optimized_data = await optimize(instance_file_path, config.optimization_quantity)
        instance_file_path = await save_file(folder, filename, optimized_data, is_rewrite=True)
    # TODO: Add webp conversion, cropping
    return {"instance": instance_file_path}


async def save_base64_image(image: Image, config: ImageConfig):
    header, _data = image.image.split(';base64,')
    image_data = base64.b64decode(_data)
    file_path = await image_process(image.filename, image_data, config)
    return file_path
