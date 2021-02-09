import os
import aiofiles

from base.utils import get_random_string


async def save_file(file_directory, filename, file, is_rewrite: bool = False):
    if not os.path.exists(file_directory):
        os.makedirs(file_directory)

    file_path = f"{file_directory}{filename}"
    if not is_rewrite:
        while True:
            if not os.path.exists(file_path):
                break
            name, extension = filename.split(".")
            filename = f"{name}_{get_random_string(5)}.{extension}"
            file_path = f"{file_directory}{filename}"
    async with aiofiles.open(file_path, "wb") as out_file:
        await out_file.write(file)
    return file_path
