"""
instagram_caption_generator.py
------------------------------
Generates a short, engaging Instagram caption written in the style of the 'grandma' persona,
based on the AI-generated image prompt and morning phrase.
"""

from logging import getLogger
from AntonIA.services.llm_client import LLMClient, query_llm

logger = getLogger("AntonIA.instagram_caption_generator")


def build_caption_prompt(phrase: str, topic: str, style: str) -> str:
    """
    Builds a natural-language prompt to generate an Instagram caption
    written by the grandma persona.

    Args:
        phrase: the morning phrase used in the image
        topic: the visual subject or theme of the image
        style: the artistic style (for context)

    Returns:
        str: A fully constructed prompt for the LLM.
    """
    return f"""
You just made a new good morning image with the following details:

- **Phrase (in Spanish):** {phrase}
- **Image topic:** {topic}
- **Image style:** {style}

Write the description (Instagram caption) for the post.
Your goal is to make it warm, emotional, and slightly humorous — like a loving grandma who knows her followers.
End it with a few relevant emojis and hashtags in Spanish (e.g. #BuenosDías #Amor #Alegría).

Respond with only the caption text, nothing else.
    """


def generate(llm_client: LLMClient, phrase: str, topic: str, style: str) -> str:
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
    prompt = build_caption_prompt(phrase, topic, style)
    logger.info("Generating Instagram caption...")
    return query_llm(llm_client, prompt)


