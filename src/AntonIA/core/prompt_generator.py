"""
phrase_generator.py
-------------------
Generates a 'good morning' phrase based on the day of the week using an AI language model.
"""

from datetime import datetime
import json

from logging import getLogger

from ..services.llm_client import LLMClient, query_llm



logger = getLogger("AntonIA.phrase_generator")


def get_day_of_week() -> str:
    """Returns the current weekday as a string, e.g., 'Monday'."""
    return datetime.now().strftime("%A")


def build_prompt(day_of_week: str, past_records: str) -> str:
    """
    Builds the prompt to be sent to the LLM to generate a morning phrase.
    Args:
        day_of_week: current day of the week as a string
    Returns:
        str: constructed prompt for the LLM
    """
    logger.info(f"Generating request for morning phrase for {day_of_week}...")
    return (
        f"Today is {day_of_week}."
        "Give me a motivational phrase in Spanish which also mentions the day of the week, "
        "then propose a topic and style in english for an image to go alongside the phrase."
        "Also define a font or writing style in english for the phrase which goes along well with the image."
        "Respond in the following JSON format only, without any additional text:"
        "{'phrase': '...', 'topic': '...', 'style': '...', 'font': '...'}"
        "Avoid overly used phrases, topics and styles from the past days: "
        f"{past_records}"
    )

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
        cleaned = {k: v.strip() for k, v in data.items() if isinstance(v, str)}
        for key in ["phrase", "topic", "style", "font"]:
            cleaned.setdefault(key, "")
        return cleaned
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from LLM response: {e}")
        raise ValueError("Malformed LLM response: not valid JSON.") from e
    
def generate_prompt(parsed_response: dict[str, str]) -> str:
    """
    Generates a prompt for an image generation model based on the parsed LLM response.
    Args:
        parsed_response: dictionary with keys 'phrase', 'topic', 'style', 'font'
    Returns:
        str: constructed prompt for image generation
    """
    phrase = parsed_response["phrase"]
    topic = parsed_response["topic"]
    style = parsed_response["style"]
    font = parsed_response["font"]

    prompt = " ".join([ 
        f"Create an image of {topic.lower()}.",
        f"Use a {style.lower()} style for the overall look and feel of the image.",
        f"Overlay the phrase '{phrase}' prominently in the image using {font}."
    ])

    logger.info(f"Generated prompt for image generation: {prompt}")

    return prompt

def generate(llm_client: LLMClient, past_records, temperature: float = 0.8) -> tuple[str, dict]:
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
    prompt = build_prompt(day_of_the_week, past_records)
    response = query_llm(llm_client, prompt, temperature)
    parsed_response = parse_response(response)
    image_prompt = generate_prompt(parsed_response)
    return image_prompt, parsed_response
