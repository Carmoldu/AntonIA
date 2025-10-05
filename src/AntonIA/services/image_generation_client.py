"""
image_generation_client.py
--------------------------
Abstraction layer for AI-based image generation services.
Currently implemented for OpenAI's Images API.
"""

import base64
from datetime import datetime
from pathlib import Path
from logging import getLogger
from typing import Protocol, Literal

from openai import OpenAI

from AntonIA.common.config import config


logger = getLogger("AntonIA.image_generation_client")



class ImageGenerationClient(Protocol):
    def generate_image(self, prompt: str, size: str = "1024x1024") -> Path:
        """Generate an image from a textual prompt and return the path to the saved image."""
        pass

class ImageGenerationClient:
    def __init__(self, model: str = "gpt-image-1", output_dir: str = "./outputs/images"):
        """
        Initialize the image generation client.

        Args:
            model: model identifier for image generation (e.g., 'gpt-image-1')
            output_dir: local directory where images will be saved
        """
        self.client = OpenAI(api_key=config.openai_api_key)
        self.model = model
        self.output_dir = Path(output_dir)

    def generate_image(
            self, 
            prompt: str, 
            size: Literal[
                '1024x1024', 
                '1024x1536', 
                '1536x1024', 
                'auto',
                ] = "1024x1024"
            ) -> Path:
        """
        Generate an image from a textual prompt and save it locally.

        Args:
            prompt: textual description of the desired image
            size: resolution (supported: '512x512', '1024x1024', etc.)

        Returns:
            Path to the saved image file
        """
        logger.info("Generating image...")
        logger.debug(f"Prompt: {prompt}")

        try:
            result = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                n=1,
                quality="auto",
            )

            image_base64 = result.data[0].b64_json
            image_bytes = bytes.fromhex("") if not image_base64 else image_base64.encode("utf-8")

            # Decode base64 properly
            image_data = base64.b64decode(image_base64)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = self.output_dir / f"image_{timestamp}_{hash(prompt) & 0xFFFFFFFF}.png"
            with open(image_path, "wb") as f:
                f.write(image_data)

            logger.info(f"Image saved to {image_path}")
            return image_path

        except Exception as e:
            logger.exception("Failed to generate image")
            raise RuntimeError("Image generation failed") from e
