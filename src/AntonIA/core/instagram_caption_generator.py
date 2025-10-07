"""
instagram_caption_generator.py
------------------------------
Generates a short, engaging Instagram caption written in the style of the 'grandma' persona,
based on the AI-generated image prompt and morning phrase.
"""

from logging import getLogger
from ..services.llm_client import LLMClient, query_llm
from ..utils.prompts import build_prompt_from_template

logger = getLogger("AntonIA.instagram_caption_generator")



def generate(llm_client: LLMClient, template: str, phrase: str, topic: str, style: str) -> str:
    """
    Uses the LLM client to generate an Instagram caption.

    Args:
        llm_client: instance of the injected LLM client
        phrase: the morning phrase that appears on the image
        topic: visual topic (e.g., 'sunrise with birds')
        style: artistic style (e.g., 'watercolor')

    Returns:
        str: generated caption text
    """
    prompt = build_prompt_from_template(template, phrase, topic, style)
    logger.info("Generating Instagram caption...")
    return query_llm(llm_client, prompt)


