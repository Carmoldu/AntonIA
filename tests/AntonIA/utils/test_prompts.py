import pytest
from AntonIA.utils.prompts import build_prompt_from_template

def test_build_prompt_from_template_basic():
    template = "Hello, {{name}}!"
    tags = {"name": "Alice"}
    result = build_prompt_from_template(template, tags)
    assert result == "Hello, Alice!"

def test_build_prompt_from_template_multiple_tags():
    template = "Dear {{title}} {{name}}, welcome to {{place}}."
    tags = {"title": "Dr.", "name": "Smith", "place": "Wonderland"}
    result = build_prompt_from_template(template, tags)
    assert result == "Dear Dr. Smith, welcome to Wonderland."

def test_build_prompt_from_template_missing_tag_raises():
    template = "Hello, {{name}}! Your code is {{status}}."
    tags = {"name": "Bob"}
    with pytest.raises(ValueError) as excinfo:
        build_prompt_from_template(template, tags)
    assert "Unreplaced placeholders" in str(excinfo.value)

def test_build_prompt_from_template_no_placeholders():
    template = "No placeholders here."
    tags = {"unused": "value"}
    result = build_prompt_from_template(template, tags)
    assert result == "No placeholders here."

def test_build_prompt_from_template_empty_tags():
    template = "Hello, {{name}}!"
    tags = {}
    with pytest.raises(ValueError):
        build_prompt_from_template(template, tags)

def test_build_prompt_from_template_placeholder_with_empty_value():
    template = "Hello, {{name}}!"
    tags = {"name": ""}
    result = build_prompt_from_template(template, tags)
    assert result == "Hello, !"