"""
llm_client.py
-------------
Wrapper around APIs for text generation.
"""

import os
from typing import Protocol

from openai import OpenAI

from AntonIA.common.config import config



class LLMClient(Protocol):
    def generate_text(self, prompt: str, temperature: float = 0.8) -> str:
        """Send a text-generation request and return the model’s text."""
        pass


class MockAIClient:
    def generate_text(self, prompt: str, temperature: float = 0.8) -> str:
        """Mock implementation for testing purposes."""
        return "This is a mock response."


class OpenAIClient:
    def __init__(self, model: str = "gpt-4.1-nano", system_prompt: str = ""):
        self.client = OpenAI(api_key=config.openai_api_key)
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
            max_tokens=1000,
        )
        return response.choices[0].message.content
