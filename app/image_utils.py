from PIL import Image, ImageEnhance
from app import config


def pixelate_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert("L")
        img_small = img.resize(
            (max(1, img.width // config.PIXEL_SIZE),
             max(1, img.height // config.PIXEL_SIZE)),
            Image.NEAREST)
        img_pixelated = img_small.resize(img.size, Image.NEAREST)
        enhancer = ImageEnhance.Brightness(img_pixelated)
        img_pixelated = enhancer.enhance(1.2)
        img_pixelated.save(config.TEMP_PIXELATED_PATH)
