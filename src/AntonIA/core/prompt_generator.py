"""
phrase_generator.py
-------------------
Generates a 'good morning' phrase based on the day of the week using an AI language model.
"""

from datetime import datetime
import json

from logging import getLogger

from ..services.llm_client import LLMClient, query_llm
from ..utils.prompts import build_prompt_from_template



logger = getLogger("AntonIA.phrase_generator")


def get_day_of_week() -> str:
    """Returns the current weekday as a string, e.g., 'Monday'."""
    return datetime.now().strftime("%A")

def parse_response(response: str) -> dict[str, str]:
    """
    Parses the LLM response to extract the phrase, topic, style, and font.
    Args:
        response: raw response string from the LLM
    Returns:
        dict: parsed response with keys 'phrase', 'topic', 'style', 'font'
    """
    logger.info("Parsing response ...")
    try:
        data = json.loads(response)
        cleaned = {k: v.strip().lower() for k, v in data.items() if k != "phrase"}
        cleaned["phrase"] = data["phrase"]
        for key in ["phrase", "topic", "style", "font"]:
            cleaned.setdefault(key, "")
        return cleaned
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from LLM response: {e}")
        raise ValueError("Malformed LLM response: not valid JSON.") from e
    

def generate(
        llm_client: LLMClient, 
        prompt_generateion_template: str,
        image_prompt_template: str, 
        past_records: str, 
        temperature: float = 0.8,
        ) -> tuple[str, dict]:
    """
    Main function to generate the morning phrase and image prompt.
    Args:
        llm_client: instance of the LLMClient abstraction (e.g., OpenAI, Anthropic, etc.)
        past_records: string summarizing past records to avoid repetition
        temperature: sampling temperature for the LLM
    Returns:
        str: generated prompt for image generation
    """
    day_of_the_week = get_day_of_week()

    prompt = build_prompt_from_template(prompt_generateion_template, {"day_of_week": day_of_the_week, "past_records": past_records})

    response = query_llm(llm_client, prompt, temperature)
    parsed_response = parse_response(response)

    image_prompt = build_prompt_from_template(image_prompt_template, parsed_response)
    logger.info(f"Image generation prompt: {image_prompt}")

    return image_prompt, parsed_response
