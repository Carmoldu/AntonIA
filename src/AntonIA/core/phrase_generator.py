"""
phrase_generator.py
-------------------
Generates a 'good morning' phrase based on the day of the week using an AI language model.
"""

from datetime import datetime

from logging import getLogger
from ..services.llm_client import LLMClient



logger = getLogger("AntonIA.phrase_generator")


def get_day_of_week() -> str:
    """Returns the current weekday as a string, e.g., 'Monday'."""
    return datetime.now().strftime("%A")


def build_prompt(day_of_week: str) -> str:
    """
    Builds the prompt to be sent to the LLM to generate a morning phrase.
    You can refine tone, language, or style here.
    """
    return (
        f"Generate an uplifting and original 'good morning' phrase for a {day_of_week}. "
        f"The phrase should be short (under 25 words), positive, and suitable to post on social media. "
        f"Do not include emojis or hashtags. Return only the phrase text."
    )


def generate(llm_client: LLMClient, day_of_week: str | None = None) -> str:
    """
    Generates a good morning phrase based on the day of the week.

    Args:
        llm_client: instance of the LLMClient abstraction (e.g., OpenAI, Anthropic, etc.)
        day_of_week: optional manual override (defaults to today)

    Returns:
        str: generated morning phrase
    """
    if day_of_week is None:
        day_of_week = get_day_of_week()

    prompt = build_prompt(day_of_week)

    logger.info(f"Generating morning phrase for {day_of_week}...")

    try:
        response = llm_client.generate_text(prompt)
        phrase = response.strip().strip('"').strip("'")
        logger.info(f"Generated phrase: {phrase}")
        return phrase
    except Exception as e:
        logger.error(f"Error generating morning phrase: {e}")
        raise
