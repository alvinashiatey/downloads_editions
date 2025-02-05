from PIL import Image, ImageEnhance
from app import config


def pixelate_image(image_path: str) -> None:
    """
    Pixelate the given image and saves the result.

    Args:
            image_path (str): The file path to the image to be pixelated.

    Returns:
            None
    """
    with Image.open(image_path) as img:
        img = img.convert("CMYK")
        img_small = img.resize(
            (max(1, img.width // config.PIXEL_SIZE),
             max(1, img.height // config.PIXEL_SIZE)),
            Image.NEAREST)
        img_pixelated = img_small.resize(img.size, Image.NEAREST)
        img_pixelated = ImageEnhance.Brightness(img_pixelated).enhance(1.2)
        img_pixelated.save(config.TEMP_PIXELATED_PATH, format="JPEG")
