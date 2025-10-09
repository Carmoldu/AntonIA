"""
This module provides abstractions and implementations for interacting with large language models (LLMs) via API clients.
It defines a protocol for LLM clients, a mock client for testing, and an OpenAI client for real API calls.
A utility function is included to query the LLM and handle logging and errors.
Classes:
    LLMClient (Protocol): Interface for LLM clients with a text generation method.
    MockAIClient: Mock implementation of LLMClient for testing purposes.
    OpenAIClient: Implementation of LLMClient using the OpenAI API.
Functions:
    query_llm(llm_client, prompt, temperature): Queries the provided LLM client with a prompt and returns the generated text.
"""

from logging import getLogger
from typing import Protocol

from openai import OpenAI



logger = getLogger("AntonIA.llm_client")

class LLMClient(Protocol):
    """
    Protocol for a Large Language Model (LLM) client.

    Defines the interface for sending text-generation requests to an LLM.

    Methods
    -------
    generate_text(prompt: str, temperature: float = 0.8) -> str
        Sends a prompt to the LLM and returns the generated text.
        Parameters:
            prompt (str): The input text to prompt the model.
            temperature (float, optional): Sampling temperature for generation. Defaults to 0.8.
        Returns:
            str: The generated text from the model.
    """
    def generate_text(self, prompt: str, temperature: float = 0.8) -> str:
        """
        Generates text from a given prompt using a language model.

        Args:
            prompt (str): The input text prompt to guide the text generation.
            temperature (float, optional): Sampling temperature for controlling randomness. Defaults to 0.8.

        Returns:
            str: The generated text from the model.
        """
        pass


class MockAIClient:
    """
    A mock implementation of an AI client for testing purposes.
    Attributes:
        response (str): The mock response to return when generating text.
    Methods:
        generate_text(prompt: str, temperature: float = 0.8) -> str:
            Returns the predefined mock response regardless of the input prompt or temperature.
    """
    def __init__(self, response: str = "This is a mock response."):
        self.response = response

    def generate_text(self, prompt: str, temperature: float = 0.8) -> str:
        """
        Generates a text response based on the given prompt and temperature.

        Args:
            prompt (str): The input prompt to generate text from.
            temperature (float, optional): Sampling temperature for text generation. Defaults to 0.8.

        Returns:
            str: The generated text response.
        """
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
