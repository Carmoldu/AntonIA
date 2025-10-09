import pytest
import json
from unittest.mock import MagicMock, patch
from AntonIA.core import prompt_generator

class DummyLLMClient:
    pass

@pytest.fixture
def valid_llm_response():
    return json.dumps({
        "phrase": "Buenos días, hoy es lunes.",
        "topic": "motivación",
        "style": "alegre",
        "font": "arial"
    })

@pytest.fixture
def malformed_llm_response():
    return "not a json string"

def test_get_day_of_week_returns_valid_day():
    day = prompt_generator.get_day_of_week()
    assert day in [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]

def test_parse_response_valid(valid_llm_response):
    result = prompt_generator.parse_response(valid_llm_response)
    assert result["phrase"] == "Buenos días, hoy es lunes."
    assert result["topic"] == "motivación"
    assert result["style"] == "alegre"
    assert result["font"] == "arial"

def test_parse_response_missing_keys():
    response = json.dumps({"phrase": "Hola"})
    result = prompt_generator.parse_response(response)
    assert result["phrase"] == "Hola"
    assert result["topic"] == ""
    assert result["style"] == ""
    assert result["font"] == ""

def test_parse_response_malformed(malformed_llm_response):
    with pytest.raises(ValueError):
        prompt_generator.parse_response(malformed_llm_response)

@patch("AntonIA.core.prompt_generator.build_prompt_from_template")
@patch("AntonIA.core.prompt_generator.query_llm")
def test_generate_calls_and_returns(mock_query_llm, mock_build_prompt):
    llm_client = DummyLLMClient()
    prompt_template = "Prompt: {day_of_week}, {past_records}, {language}"
    image_template = "Image: {phrase}, {topic}, {style}, {font}, {language}"
    past_records = "No repetition"
    temperature = 0.5
    language = "spanish"

    mock_build_prompt.side_effect = [
        "built_prompt",  # for phrase generation
        "built_image_prompt"  # for image generation
    ]
    mock_query_llm.return_value = json.dumps({
        "phrase": "Buenos días!",
        "topic": "motivación",
        "style": "alegre",
        "font": "arial"
    })

    image_prompt, parsed_response = prompt_generator.generate(
        llm_client,
        prompt_template,
        image_template,
        past_records,
        temperature,
        language
    )

    assert image_prompt == "built_image_prompt"
    assert parsed_response["phrase"] == "Buenos días!"
    assert parsed_response["topic"] == "motivación"
    assert parsed_response["style"] == "alegre"
    assert parsed_response["font"] == "arial"
    assert parsed_response["language"] == "spanish"
    assert mock_build_prompt.call_count == 2
    mock_query_llm.assert_called_once()