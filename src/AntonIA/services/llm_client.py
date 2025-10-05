"""
llm_client.py
-------------
Wrapper around APIs for text generation.
"""

import os
from typing import Protocol



class LLMClient(Protocol):
    def generate_text(self, prompt: str, temperature: float = 0.8) -> str:
        """Send a text-generation request and return the model’s text."""
        pass


class MockAIClient:
    def generate_text(self, prompt: str, temperature: float = 0.8) -> str:
        """Mock implementation for testing purposes."""
        return "This is a mock response."

