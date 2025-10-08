"""
llm_client.py
-------------
Wrapper around APIs for text generation.
"""

import os
from logging import getLogger
from typing import Protocol

from openai import OpenAI



logger = getLogger("AntonIA.llm_client")

class LLMClient(Protocol):
    def generate_text(self, prompt: str, temperature: float = 0.8) -> str:
        """Send a text-generation request and return the model’s text."""
        pass


class MockAIClient:
    def __init__(self, response: str = "This is a mock response."):
        self.response = response

    def generate_text(self, prompt: str, temperature: float = 0.8) -> str:
        """Mock implementation for testing purposes."""
        return self.response


class OpenAIClient:
    def __init__(self, api_key, model: str = "gpt-4.1-nano", system_prompt: str = ""):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt

    def generate_text(self, prompt: str, temperature: float = 0.8) -> str:
        """Send a text-generation request and return the model’s text."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
                ],
            temperature=temperature,
        )
        return response.choices[0].message.content

def query_llm(llm_client: LLMClient, prompt: str, temperature: float = 0.8) -> str:
    """
    Generates a good morning phrase based on the day of the week.

    Args:
        llm_client: instance of the LLMClient abstraction (e.g., OpenAI, Anthropic, etc.)
        prompt: text prompt to send to the LLM
    Returns:
        str: response of the LLM
    """
    logger.info("Querying LLM...")
    try:
        response = llm_client.generate_text(prompt, temperature=temperature)
        logger.info(f"LLM response: {response}")
        return response
    except Exception as e:
        logger.exception("Error querying LLM.")
        raise RuntimeError("Failed to query the LLM.") from e
