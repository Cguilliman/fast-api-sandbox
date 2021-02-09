from PIL import Image
from io import BytesIO
import aiofiles


QUALITY = 90


async def optimize(file_path, optimize_quality: int = QUALITY):
    filename = file_path.rsplit("/", 1)[-1]
    name, extension = filename.rsplit(".", 1)
    extension = extension.capitalize()

    image = Image.open(file_path)
    bytes_io = BytesIO()

    if image.mode in ('RGBA', 'LA'):
        background = (
            Image.new(image.mode[:-1], image.size, '#FFFFFF')
        )
        background.paste(image, image.split()[-1])
        image = background

    save_kwargs = {
        'format': extension,
        'optimize': True,
        'quality': optimize_quality,
    }

    if extension == 'WEBP':
        save_kwargs['lossless'] = True
    elif extension == 'JPEG':
        save_kwargs['progressive'] = True

    image.save(
        bytes_io,
        **save_kwargs
    )
    buffer = bytes_io.getvalue()
    return buffer
