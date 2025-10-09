import pytest
from AntonIA.services.llm_client import OpenAIClient, MockAIClient, query_llm

class DummyOpenAIChatCompletions:
    def create(self, model, messages, temperature):
        class DummyResponse:
            class Choices:
                class Message:
                    content = "Dummy OpenAI response."
                message = Message()
            choices = [Choices()]
        return DummyResponse()

class DummyOpenAIClient:
    def __init__(self, api_key):
        self.chat = type('Chat', (), {'completions': DummyOpenAIChatCompletions()})()

def test_mock_ai_client_generate_text():
    mock_client = MockAIClient(response="Test response")
    result = mock_client.generate_text("Hello", temperature=0.5)
    assert result == "Test response"

def test_query_llm_with_mock_client():
    mock_client = MockAIClient(response="Mocked output")
    prompt = "Say hello"
    result = query_llm(mock_client, prompt)
    assert result == "Mocked output"

def test_openai_client_generate_text(monkeypatch):
    # Patch OpenAI to use DummyOpenAIClient
    monkeypatch.setattr("AntonIA.services.llm_client.OpenAI", lambda api_key: DummyOpenAIClient(api_key))
    client = OpenAIClient(api_key="fake-key", model="gpt-4.1-nano", system_prompt="You are helpful.")
    result = client.generate_text("Hello world", temperature=0.7)
    assert result == "Dummy OpenAI response."

def test_query_llm_with_openai_client(monkeypatch):
    monkeypatch.setattr("AntonIA.services.llm_client.OpenAI", lambda api_key: DummyOpenAIClient(api_key))
    client = OpenAIClient(api_key="fake-key")
    prompt = "Good morning!"
    result = query_llm(client, prompt)
    assert result == "Dummy OpenAI response."