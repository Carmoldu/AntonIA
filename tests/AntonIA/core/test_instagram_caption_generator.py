import pytest
from unittest.mock import MagicMock, patch
from AntonIA.core import instagram_caption_generator

@pytest.fixture
def mock_llm_client():
    return MagicMock()

@pytest.fixture
def mock_build_prompt():
    with patch("AntonIA.core.instagram_caption_generator.build_prompt_from_template") as mock:
        yield mock

@pytest.fixture
def mock_query_llm():
    with patch("AntonIA.core.instagram_caption_generator.query_llm") as mock:
        yield mock

def test_generate_calls_build_prompt_and_query_llm(
    mock_llm_client, mock_build_prompt, mock_query_llm
):
    # Arrange
    template = "template"
    phrase = "Good morning!"
    topic = "sunrise with birds"
    style = "watercolor"
    language = "en"
    hashtags = "#morning #sunrise"
    temperature = 0.7
    prompt = "built prompt"
    mock_build_prompt.return_value = prompt
    mock_query_llm.return_value = "Generated caption"

    # Act
    result = instagram_caption_generator.generate(
        mock_llm_client,
        temperature,
        template,
        phrase,
        topic,
        style,
        language,
        hashtags,
    )

    # Assert
    mock_build_prompt.assert_called_once_with(
        template,
        {
            "phrase": phrase,
            "topic": topic,
            "style": style,
            "language": language,
            "hashtags": hashtags,
        }
    )
    mock_query_llm.assert_called_once_with(mock_llm_client, prompt, temperature=temperature)
    assert result == "Generated caption"

def test_generate_returns_string(
    mock_llm_client, mock_build_prompt, mock_query_llm
):
    mock_build_prompt.return_value = "prompt"
    mock_query_llm.return_value = "Some caption"
    result = instagram_caption_generator.generate(
        mock_llm_client, 0.5, "tpl", "phrase", "topic", "style", "lang", "tags"
    )
    assert isinstance(result, str)