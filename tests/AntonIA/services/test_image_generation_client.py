import pytest
from AntonIA.services.image_generation_client import MockImageGenerationClient
from AntonIA.services.image_generation_client import OpenAIimageGenerationClient

def test_mock_image_generation_client_returns_bytes():
    client = MockImageGenerationClient()
    result = client.generate_image("A cat sitting on a sofa")
    assert isinstance(result, bytes)
    assert len(result) > 0

def test_mock_image_generation_client_image_is_png():
    client = MockImageGenerationClient()
    result = client.generate_image("A sunset over the mountains")
    # PNG files start with these bytes
    assert result[:8] == b'\x89PNG\r\n\x1a\n'

def test_mock_image_generation_client_same_image_for_different_prompts():
    client = MockImageGenerationClient()
    img1 = client.generate_image("Prompt 1")
    img2 = client.generate_image("Prompt 2")
    assert img1 == img2

def test_mock_image_generation_client_size_argument_is_ignored():
    client = MockImageGenerationClient()
    img_default = client.generate_image("Test", size="1024x1024")
    img_other = client.generate_image("Test", size="512x512")
    assert img_default == img_other

class DummyOpenAI:
    class images:
        @staticmethod
        def generate(model, prompt, size, n, quality):
            class Result:
                data = [type("obj", (), {"b64_json": "iVBORw0KGgoAAAANSUhEUgAAAAUA"})]
            return Result()

def test_openai_image_generation_client_returns_bytes(monkeypatch):
    # Patch OpenAI to DummyOpenAI
    monkeypatch.setattr("AntonIA.services.image_generation_client.OpenAI", lambda api_key: DummyOpenAI)
    client = OpenAIimageGenerationClient(api_key="fake-key")
    result = client.generate_image("A test prompt")
    assert isinstance(result, bytes)
    assert result[:8] == b'\x89PNG\r\n\x1a\n'[:len(result)]

def test_openai_image_generation_client_raises_on_exception(monkeypatch):
    class FailingDummyOpenAI:
        class images:
            @staticmethod
            def generate(*args, **kwargs):
                raise Exception("API error")
    monkeypatch.setattr("AntonIA.services.image_generation_client.OpenAI", lambda api_key: FailingDummyOpenAI)
    client = OpenAIimageGenerationClient(api_key="fake-key")
    with pytest.raises(RuntimeError, match="Image generation failed"):
        client.generate_image("A test prompt")
