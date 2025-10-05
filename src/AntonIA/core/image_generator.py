"""
image_generator.py
------------------
Handles the orchestration of AI image generation from prompts.
"""

from logging import getLogger
from pathlib import Path

from ..services.image_generation_client import ImageGenerationClient

logger = getLogger("AntonIA.image_generator")


def generate(prompt: str, size: str = "1024x1024") -> Path:
    """
    Generate an image given a prompt.

    Args:
        prompt: text describing the image to create
        size: resolution (default: 1024x1024)

    Returns:
        Path to the generated image file
    """
    logger.info("Starting image generation process...")

    client = ImageGenerationClient()
    image_path = client.generate_image(prompt, size)

    logger.info(f"Image generated successfully: {image_path}")
    return image_path
