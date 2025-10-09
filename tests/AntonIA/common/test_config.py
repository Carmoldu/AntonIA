import os
import tempfile
import shutil
from pathlib import Path
import pytest
import yaml
from AntonIA.common import config

@pytest.fixture
def config_dir(tmp_path):
    # Create config directory structure
    config_path = tmp_path / "config"
    personas_path = config_path / "personas"
    config_path.mkdir()
    personas_path.mkdir()

    # Create base.yaml
    base_yaml = {
        "LLM": {
            "model": "test-llm-model",
            "temperature": 0.5,
            "api_key": "base-api-key"
        },
        "image": {
            "model": "test-image-model",
            "size": "512x512",
            "storage_path": "/tmp/images"
        },
        "database": {
            "past_records_path": "/tmp/past_records.db",
            "past_records_to_retrieve": 5
        }
    }
    with open(config_path / "base.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(base_yaml, f)

    # Create default persona
    default_persona_yaml = {
        "grandma": {
            "name": "Abuela",
            "language": "spanish",
            "hashtags": "#hola #test"
        },
        "prompts": {
            "system": "You are a helpful grandma.",
            "creation_template": "Create a story.",
            "image_template": "Generate an image.",
            "instagram_caption_template": "Caption for Instagram."
        }
    }
    with open(personas_path / "default.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(default_persona_yaml, f)

    # Create persona override
    persona_override_yaml = {
        "grandma": {
            "name": "Nonna",
            "language": "italian",
            "hashtags": "#ciao #test",
            "watermark_path": "/tmp/watermark.png"
        },
        "prompts": {
            "system": "You are a wise nonna.",
            "creation_template": "Racconta una storia.",
            "image_template": "Crea un'immagine.",
            "instagram_caption_template": "Didascalia per Instagram."
        }
    }
    with open(personas_path / "nonna.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(persona_override_yaml, f)

    return str(config_path)

def test_load_config_default_persona(config_dir, monkeypatch):
    monkeypatch.setenv(config.ENV_OPENAI_API_KEY, "env-api-key")
    cfg = config.load_config(config_dir=config_dir)
    assert cfg.grandma.name == "Abuela"
    assert cfg.llm.api_key == "env-api-key"
    assert cfg.llm.model == "test-llm-model"
    assert cfg.llm.temperature == 0.5
    assert cfg.llm.system_prompt == "You are a helpful grandma."
    assert cfg.image.model == "test-image-model"
    assert cfg.image.size == "512x512"
    assert cfg.image.storage_path == "/tmp/images"
    assert cfg.prompts.creation_template == "Create a story."
    assert cfg.prompts.image_gen_template == "Generate an image."
    assert cfg.prompts.instagram_caption_template == "Caption for Instagram."
    assert cfg.database.past_records_path == "/tmp/past_records.db"
    assert cfg.database.runs_table_name == "Abuela_runs"
    assert cfg.database.past_records_to_retrieve == 5

def test_load_config_persona_override(config_dir):
    # Remove env var to test fallback to base.yaml
    os.environ.pop(config.ENV_OPENAI_API_KEY, None)
    cfg = config.load_config(persona="nonna", config_dir=config_dir)
    assert cfg.grandma.name == "Nonna"
    assert cfg.grandma.language == "italian"
    assert cfg.grandma.hashtags == "#ciao #test"
    assert cfg.grandma.watermark_path == "/tmp/watermark.png"
    assert cfg.llm.api_key == "base-api-key"
    assert cfg.llm.system_prompt == "You are a wise nonna."
    assert cfg.prompts.creation_template == "Racconta una storia."
    assert cfg.prompts.image_gen_template == "Crea un'immagine."
    assert cfg.prompts.instagram_caption_template == "Didascalia per Instagram."
    assert cfg.database.runs_table_name == "Nonna_runs"
    assert cfg.database.past_records_path == "/tmp/past_records.db"
    assert cfg.database.past_records_to_retrieve == 5
    assert cfg.llm.model == "test-llm-model"
    assert cfg.llm.temperature == 0.5
    assert cfg.image.model == "test-image-model"
    assert cfg.image.size == "512x512"
    assert cfg.image.storage_path == "/tmp/images"

def test_missing_api_key_raises(config_dir, monkeypatch):
    # Remove env var and base.yaml key
    monkeypatch.delenv(config.ENV_OPENAI_API_KEY, raising=False)
    base_path = Path(config_dir) / "base.yaml"
    base_yaml = yaml.safe_load(base_path.read_text())
    base_yaml["LLM"].pop("api_key", None)
    with open(base_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(base_yaml, f)
    with pytest.raises(config.ConfigError):
        config.load_config(config_dir=config_dir)

def test_missing_prompt_keys_raises(config_dir):
    # Remove a prompt key from default persona
    persona_path = Path(config_dir) / "personas" / "default.yaml"
    persona_yaml = yaml.safe_load(persona_path.read_text())
    persona_yaml["prompts"].pop("creation_template", None)
    with open(persona_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(persona_yaml, f)
    with pytest.raises(config.ConfigError):
        config.load_config(config_dir=config_dir)

def test_missing_grandma_name_raises(config_dir):
    persona_path = Path(config_dir) / "personas" / "default.yaml"
    persona_yaml = yaml.safe_load(persona_path.read_text())
    persona_yaml["grandma"].pop("name", None)
    with open(persona_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(persona_yaml, f)
    with pytest.raises(config.ConfigError):
        config.load_config(config_dir=config_dir)

def test_list_personas(config_dir):
    personas = config.list_personas(config_dir=config_dir)
    assert set(personas) == {"default", "nonna"}

def test_list_personas_empty(tmp_path):
    config_path = tmp_path / "config"
    config_path.mkdir()
    personas = config.list_personas(config_dir=str(config_path))
    assert personas == []