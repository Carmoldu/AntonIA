from PIL import Image, UnidentifiedImageError
from typing import Callable, Optional
from io import BytesIO
import os



def add_watermark(image_bytes: bytes, watermark_path: str, opacity: float = 0.8, scale: float = 0.2) -> bytes:
    """
    Adds a watermark to the bottom-right corner of an image.

    Args:
        image_bytes: the original image as bytes
        watermark_path: path to the watermark image
        opacity: transparency of the watermark (0.0–1.0)
        scale: fraction of image width for watermark size (0.2 = 20%)

    Returns:
        New image as bytes (PNG)
    """

    # Open base image and watermark
    base = Image.open(BytesIO(image_bytes)).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")

    # Resize watermark relative to image size
    w_scale = int(base.width * scale)
    w_ratio = w_scale / watermark.width
    new_size = (w_scale, int(watermark.height * w_ratio))
    watermark = watermark.resize(new_size, Image.Resampling.LANCZOS)

    # Adjust transparency
    if opacity < 1:
        alpha = watermark.split()[3]
        alpha = alpha.point(lambda p: int(p * opacity))
        watermark.putalpha(alpha)

    # Paste watermark bottom-right
    position = (base.width - watermark.width - 10, base.height - watermark.height - 10)
    base.alpha_composite(watermark, dest=position)

    # Export final image
    output = BytesIO()
    base.convert("RGB").save(output, format="PNG")
    return output.getvalue()

def add_watermark_fn_factory(
    watermark_path: str, opacity: float = 0.8, scale: float = 0.2
) -> Optional[Callable[[bytes], bytes]]:
    """
    Factory that returns a watermarking function if the watermark exists and is valid.
    
    Args:
        watermark_path: path to the watermark image
        opacity: transparency of the watermark (0.0–1.0)
        scale: relative width of the watermark compared to the base image

    Returns:
        A function that takes image_bytes and returns watermarked bytes,
        or None if the watermark is missing/invalid.
    """
    # Check if file exists
    if not watermark_path or not os.path.exists(watermark_path):
        return None

    # Check if it's a valid image
    try:
        with Image.open(watermark_path) as img:
            img.verify()  # Verify it’s an image file
    except (UnidentifiedImageError, OSError):
        return None

    # If all checks pass, return the watermarking function
    def watermark_fn(image_bytes: bytes) -> bytes:
        from .image_utils import add_watermark  # import here if circular imports possible
        return add_watermark(image_bytes, watermark_path, opacity, scale)

    return watermark_fn
