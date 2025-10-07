"""
image_generator.py
------------------
Handles the orchestration of AI image generation from prompts.
"""

from logging import getLogger
from typing import Callable, Optional

from ..services.image_generation_client import ImageGenerationClient



logger = getLogger("AntonIA.image_generator")


image_processing_fn_signature = Callable[[bytes], bytes]

def generate(client: ImageGenerationClient, prompt: str, size: str = "1024x1024", postprocess_fn: Optional[image_processing_fn_signature] = None) -> bytes:
    """
    Generate an image given a prompt.

    Args:
        prompt: text describing the image to create
        size: resolution (default: 1024x1024)

    Returns:
        Path to the generated image file
    """
    logger.info("Starting image generation process...")

    image_bytes = client.generate_image(prompt, size)
    logger.info(f"Image generated successfully")

    if postprocess_fn:
        image_bytes = postprocess_fn(image_bytes)

    return image_bytes
