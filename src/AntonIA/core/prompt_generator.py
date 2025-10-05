"""
phrase_generator.py
-------------------
Generates a 'good morning' phrase based on the day of the week using an AI language model.
"""

from datetime import datetime
import json

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
        f"Today is {day_of_week}."
        f"Give me a motivational phrase in Spanish which also mentions the day of the week, "
        f"then propose a topic and style in english for an image to go alongside the phrase."
        f"Also define a font or writing style in english for the phrase which goes along well with the image."
        f"Respond in the following JSON format only, without any additional text:"
        f'{{"phrase": "...", "topic": "...", "style": "...", "font": "..."}}'
    )


def query_llm(llm_client: LLMClient, day_of_week: str | None = None) -> str:
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


def parse_response(response: str) -> dict:
    """
    Parses the LLM response to extract the phrase, topic, style, and font.
    Args:
        response: raw response string from the LLM
    Returns:
        dict: parsed response with keys 'phrase', 'topic', 'style', 'font'
    """
    try:
        data = json.loads(response)
        return {
            "phrase": data.get("phrase", "").strip(),
            "topic": data.get("topic", "").strip(),
            "style": data.get("style", "").strip(),
            "font": data.get("font", "").strip(),
        }
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing LLM response: {e}")
        raise ValueError("Failed to parse LLM response as JSON.") from e
    
def generate_prompt(parsed_response: dict) -> str:
    """
    Generates a prompt for an image generation model based on the parsed LLM response.
    Args:
        parsed_response: dictionary with keys 'phrase', 'topic', 'style', 'font'
    Returns:
        str: constructed prompt for image generation
    """
    phrase = parsed_response.get("phrase", "")
    topic = parsed_response.get("topic", "")
    style = parsed_response.get("style", "")
    font = parsed_response.get("font", "")

    prompt = " ".join([ 
        f"Create an image of {topic.lower()}",
        f"Use a {style.lower()} style for the overall look and feel of the image.",
        f"Overlay the phrase '{phrase}' prominently in the image using {font}",
        "The image should evoke positive and uplifting emotions suitable for a good morning greeting."
    ])

    logger.info(f"Generated prompt for image generation: {prompt}")

    return prompt

def generate(llm_client: LLMClient, day_of_week: str | None = None) -> dict:
    """
    Main function to generate the morning phrase and image prompt.
    Args:
        llm_client: instance of the LLMClient abstraction (e.g., OpenAI, Anthropic, etc.)
        day_of_week: optional manual override (defaults to today)
    Returns:
        str: generated prompt for image generation
    """
    response = query_llm(llm_client, day_of_week)
    parsed_response = parse_response(response)
    image_prompt = generate_prompt(parsed_response)
    return image_prompt
