import os

from base.utils import get_random_string
from .optimizer import optimize, crop, convert_to_webp
from .config import ImageConfig
from ..base import save_file


def get_file_folder(base_folder, filename):
    name, _ = filename.rsplit(".", 1)
    path = f"{base_folder}{name}/"
    while True:
        if not os.path.exists(path):
            break
        name = f"{name}_{get_random_string(3)}"
        path = f"{base_folder}{name}/"
    return path


def directory_and_file(directory, file):
    directory = f"{directory}/" if not directory.endswith("/") else directory
    return f"{directory}{file}"


class ImageService:

    def __init__(self, file_path: str, config: ImageConfig):
        self.config = config
        self.file_path = file_path
        self.folder, self.filename = file_path.rsplit("/", 1)
        self._filename, self.extension = self.filename.rsplit(".", 1)

    async def get_optimized(self):
        optimized_data = optimize(self.file_path, self.config.optimization_quantity)
        return await save_file(self.folder, self.filename, optimized_data, is_rewrite=True)

    async def get_webp(self, is_update=False):
        # Build webp file name
        filename = f"{self._filename}.webp"
        # Build webp file path
        webp_file_path = directory_and_file(self.folder, filename)
        if is_update or not os.path.exists(webp_file_path):
            webp_data = convert_to_webp(self.file_path)
            return await save_file(self.folder, filename, webp_data, is_rewrite=True)
        return webp_file_path

    async def get_crop(self, width, height, ppoi=(0.5, 0.5), is_webp=False, is_update=False):
        extension = "webp" if is_webp else self.extension
        filename = f"{self._filename}_{width}x{height}.{extension}"
        crop_file_path = directory_and_file(self.folder, filename)
        if is_update or not os.path.exists(crop_file_path):
            file_path = await self.get_webp() if is_webp else self.file_path
            image_data = crop(width, height, file_path, ppoi)
            return await save_file(self.folder, filename, image_data, is_rewrite=True)
        return crop_file_path

    async def generate_crops(self):
        for size in self.config.sizes:
            if self.config.is_webp:
                await self.get_crop(**size, is_webp=True, is_update=True)
            await self.get_crop(**size, is_update=True)

    @classmethod
    async def save(cls, image_data, filename: str, uploads_path: str, config: ImageConfig):
        base_folder = (
            f"{uploads_path}{config.folder}/"
            if config.folder else uploads_path
        )
        folder = get_file_folder(base_folder, filename)
        # Save instance image file
        instance_file_path = await save_file(folder, filename, image_data)
        service = cls(
            file_path=instance_file_path,
            config=config
        )
        if config.is_optimizer:
            await service.get_optimized()
        if config.is_webp:
            await service.get_webp()
        if config.sizes:
            await service.generate_crops()
        return service
