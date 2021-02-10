from PIL import Image
from io import BytesIO


QUALITY = 90


def optimize(file_path, optimize_quality: int = QUALITY):
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


def convert_to_webp(file_path):
    image = Image.open(file_path).convert("RGB")
    bytes_io = BytesIO()
    image.save(bytes_io, "webp")
    buffer = bytes_io.getvalue()
    return buffer


def crop(width, height, file_path, ppoi=(0.5, 0.5)):
    image = Image.open(file_path)
    ppoi_x_axis, ppoi_y_axis = (
        int(image.size[0] * ppoi[0]),
        int(image.size[1] * ppoi[1])
    )
    orig_aspect_ratio = float(
        image.size[0]
    ) / float(
        image.size[1]
    )
    crop_aspect_ratio = float(width) / float(height)

    # Figure out if we're trimming from the left/right or top/bottom
    if orig_aspect_ratio >= crop_aspect_ratio:
        # `image` is wider than what's needed,
        # crop from left/right sides
        orig_crop_width = int(
            (crop_aspect_ratio * float(image.size[1])) + 0.5
        )
        orig_crop_height = image.size[1]
        crop_boundary_top = 0
        crop_boundary_bottom = orig_crop_height
        crop_boundary_left = ppoi_x_axis - (orig_crop_width // 2)
        crop_boundary_right = crop_boundary_left + orig_crop_width
        if crop_boundary_left < 0:
            crop_boundary_left = 0
            crop_boundary_right = crop_boundary_left + orig_crop_width
        elif crop_boundary_right > image.size[0]:
            crop_boundary_right = image.size[0]
            crop_boundary_left = image.size[0] - orig_crop_width

    else:
        # `image` is taller than what's needed,
        # crop from top/bottom sides
        orig_crop_width = image.size[0]
        orig_crop_height = int(
            (float(image.size[0]) / crop_aspect_ratio) + 0.5
        )
        crop_boundary_left = 0
        crop_boundary_right = orig_crop_width
        crop_boundary_top = ppoi_y_axis - (orig_crop_height // 2)
        crop_boundary_bottom = crop_boundary_top + orig_crop_height
        if crop_boundary_top < 0:
            crop_boundary_top = 0
            crop_boundary_bottom = crop_boundary_top + orig_crop_height
        elif crop_boundary_bottom > image.size[1]:
            crop_boundary_bottom = image.size[1]
            crop_boundary_top = image.size[1] - orig_crop_height
    # Cropping the image from the original image
    cropped_image = image.crop(
        (
            crop_boundary_left,
            crop_boundary_top,
            crop_boundary_right,
            crop_boundary_bottom
        )
    )
    # Resizing the newly cropped image to the size specified
    # (as determined by `width`x`height`)
    # bytes_io = BytesIO()
    cropped_image.resize(
        (width, height),
        Image.ANTIALIAS
    )
    bytes_io = BytesIO()
    extension = file_path.rsplit(".", 1)[-1]
    cropped_image.save(bytes_io, format=extension)
    buffer = bytes_io.getvalue()
    return buffer
