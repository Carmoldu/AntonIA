import pytest
from unittest.mock import Mock
from AntonIA.core.image_generator import generate

class DummyClient:
    def generate_image(self, prompt, size):
        return b"fake_image_bytes"

def test_generate_returns_image_bytes():
    client = DummyClient()
    prompt = "A cat riding a bike"
    result = generate(client, prompt)
    assert isinstance(result, bytes)
    assert result == b"fake_image_bytes"

def test_generate_calls_postprocess_fn():
    client = DummyClient()
    prompt = "A dog in space"
    postprocess_fn = Mock(return_value=b"processed_bytes")
    result = generate(client, prompt, postprocess_fn=postprocess_fn)
    postprocess_fn.assert_called_once_with(b"fake_image_bytes")
    assert result == b"processed_bytes"

def test_generate_with_custom_size():
    client = DummyClient()
    prompt = "A sunset"
    size = "512x512"
    result = generate(client, prompt, size=size)
    assert result == b"fake_image_bytes"