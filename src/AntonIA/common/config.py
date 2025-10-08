# src/AntonIA/common/config.py
from __future__ import annotations

import os
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List

from dotenv import load_dotenv
import yaml

logger = logging.getLogger(__name__)

# -------------------------
# Constants (centralized defaults / "magic" strings)
# -------------------------
DEFAULT_CONFIG_DIR = "./config"
BASE_CONFIG_FILE = "base.yaml"
PERSONAS_DIR = "personas"
DEFAULT_PERSONA_FILE = "default.yaml"

# Environment variable names
ENV_OPENAI_API_KEY = "OPENAI_API_KEY"

# Default model / runtime defaults
DEFAULT_LLM_MODEL = "gpt-4.1-nano"
DEFAULT_LLM_TEMPERATURE = 0.8

DEFAULT_IMAGE_MODEL = "gpt-image-1-mini"
DEFAULT_IMAGE_SIZE = "1024x1024"
DEFAULT_IMAGE_STORAGE_PATH = "./outputs/images"

# Database keys / defaults
DEFAULT_DB_PAST_RECORDS_KEY = "past_records_path"
DEFAULT_DB_PAST_RECORDS_TO_RETRIEVE = 10

# Prompt keys tolerated in persona yaml
PROMPT_KEY_SYSTEM = "system"
PROMPT_KEY_CREATION = "creation_template"
PROMPT_KEY_IMAGE = "image_template"
PROMPT_KEY_INSTAGRAM = "instagram_caption_template"

# -------------------------
# Exceptions / dataclasses
# -------------------------
class ConfigError(RuntimeError):
    """Raised when configuration loading/validation fails."""


@dataclass
class LLMConfig:
    api_key: str
    model: str
    temperature: float
    system_prompt: str


@dataclass
class ImageConfig:
    api_key: Optional[str]
    model: str
    size: str
    storage_path: str


@dataclass
class PromptsConfig:
    creation_template: str
    image_gen_template: str
    instagram_caption_template: str


@dataclass
class DatabaseConfig:
    past_records_path: str
    runs_table_name: str
    past_records_to_retrieve: int


@dataclass
class GrandmaConfig:
    name: str
    language: str
    watermark_path: Optional[str] = None

    @property
    def runs_table_name(self) -> str:
        return f"{self.name}_runs"


@dataclass
class Config:
    grandma: GrandmaConfig
    llm: LLMConfig
    image: ImageConfig
    prompts: PromptsConfig
    database: DatabaseConfig


# -------------------------
# Small helpers
# -------------------------
def load_yaml(path: Path) -> Dict[str, Any]:
    """Load YAML file returning an empty dict if missing."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def update_dict(d: dict, u: dict) -> dict:
    """Recursive merge: update d with u, returning d modified."""
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def first_present(d: dict, *keys, default=None):
    """Return first existing key value from d or default."""
    for k in keys:
        if k in d:
            return d[k]
    return default


# -------------------------
# Small SRP functions
# -------------------------
def _read_base_config(config_dir: str) -> Dict[str, Any]:
    base_path = Path(config_dir) / BASE_CONFIG_FILE
    return load_yaml(base_path)


def _read_default_persona(config_dir: str) -> Dict[str, Any]:
    default_persona_path = Path(config_dir) / PERSONAS_DIR / DEFAULT_PERSONA_FILE
    return load_yaml(default_persona_path)


def _read_persona_override(config_dir: str, persona: str) -> Dict[str, Any]:
    persona_path = Path(config_dir) / PERSONAS_DIR / f"{persona}.yaml"
    if not persona_path.exists():
        raise FileNotFoundError(f"Persona configuration file not found: {persona_path}")
    return load_yaml(persona_path)


def _merge_persona_configs(default_persona: Dict[str, Any], persona_override: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(default_persona)  # shallow copy
    if persona_override:
        merged = update_dict(merged, persona_override)
    return merged


def _resolve_api_key(base_config: Dict[str, Any]) -> str:
    env_key = os.getenv(ENV_OPENAI_API_KEY)
    if env_key:
        return env_key
    # legacy/backwards compatible key in base config
    alt = base_config.get("OPENAI_API_KEY") or base_config.get("llm_api_key") or base_config.get("LLM", {}).get("api_key")
    if alt:
        return alt
    raise ConfigError(f"{ENV_OPENAI_API_KEY} not found in environment or base config.")


def _build_llm_config(base_config: Dict[str, Any], persona_prompts: Dict[str, Any], api_key: str) -> LLMConfig:
    llm = base_config.get("LLM", base_config.get("llm", {}))
    model = llm.get("model", DEFAULT_LLM_MODEL)
    temperature = float(llm.get("temperature", DEFAULT_LLM_TEMPERATURE))

    # system prompt is typically defined in persona prompts under 'system'
    system_prompt = first_present(persona_prompts, PROMPT_KEY_SYSTEM, "system_prompt", default="")

    return LLMConfig(api_key=api_key, model=model, temperature=temperature, system_prompt=system_prompt)


def _build_image_config(base_config: Dict[str, Any], api_key: str) -> ImageConfig:
    image = base_config.get("image", {})
    return ImageConfig(
        api_key=api_key,
        model=image.get("model", DEFAULT_IMAGE_MODEL),
        size=image.get("size", DEFAULT_IMAGE_SIZE),
        storage_path=image.get("storage_path", DEFAULT_IMAGE_STORAGE_PATH),
    )


def _build_database_config(base_config: Dict[str, Any], grandma_name: str) -> DatabaseConfig:
    db = base_config.get("database", {})
    if DEFAULT_DB_PAST_RECORDS_KEY not in db and "past_records_database_path" not in db:
        raise ConfigError(f"Missing '{DEFAULT_DB_PAST_RECORDS_KEY}' in base config -> database section.")
    past_records_path = db.get(DEFAULT_DB_PAST_RECORDS_KEY, db.get("past_records_database_path"))
    past_records_to_retrieve = int(db.get("past_records_to_retrieve", DEFAULT_DB_PAST_RECORDS_TO_RETRIEVE))
    runs_table_name = f"{grandma_name}_runs"
    return DatabaseConfig(
        past_records_path=past_records_path,
        runs_table_name=runs_table_name,
        past_records_to_retrieve=past_records_to_retrieve,
    )


def _build_prompts_config(persona_prompts: Dict[str, Any]) -> PromptsConfig:
    # accept multiple possible key names for tolerance
    prompt_creation = first_present(persona_prompts, PROMPT_KEY_CREATION)
    image_prompt = first_present(persona_prompts, PROMPT_KEY_IMAGE)
    instagram_prompt = first_present(persona_prompts, PROMPT_KEY_INSTAGRAM)

    missing = [k for k, v in (
        (PROMPT_KEY_CREATION, prompt_creation),
        (PROMPT_KEY_IMAGE, image_prompt),
        (PROMPT_KEY_INSTAGRAM, instagram_prompt),
    ) if not v]

    if missing:
        raise ConfigError(f"Missing prompt templates in persona 'prompts': {missing}")

    return PromptsConfig(
        creation_template=prompt_creation,
        image_gen_template=image_prompt,
        instagram_caption_template=instagram_prompt,
    )


def _build_grandma_config(persona_grandma: Dict[str, Any]) -> GrandmaConfig:
    if not persona_grandma or "name" not in persona_grandma:
        raise ConfigError("Persona 'grandma.name' is required in persona YAML.")
    return GrandmaConfig(
        name=persona_grandma["name"],
        language=persona_grandma.get("language", "spanish"),
        watermark_path=persona_grandma.get("watermark_path"),
    )


# -------------------------
# Public API: load_config
# -------------------------
def load_config(persona: Optional[str] = None, config_dir: str = DEFAULT_CONFIG_DIR) -> Config:
    """
    Load merged configuration and return a Config dataclass.
    - persona: optional persona filename (without .yaml) that overrides default persona.
    - config_dir: path to config directory.
    """
    load_dotenv()  # populate env vars first

    base_config = _read_base_config(config_dir)
    default_persona = _read_default_persona(config_dir)

    # If persona override is provided, merge it in
    if persona:
        persona_override = _read_persona_override(config_dir, persona)
        persona_config = _merge_persona_configs(default_persona, persona_override)
    else:
        persona_config = default_persona

    # persona_config expected keys: 'grandma' and 'prompts'
    persona_grandma = persona_config.get("grandma", {})
    persona_prompts = persona_config.get("prompts", {})

    # Resolve API key and build configs
    api_key = _resolve_api_key(base_config)
    grandma_cfg = _build_grandma_config(persona_grandma)
    llm_cfg = _build_llm_config(base_config, persona_prompts, api_key)
    image_cfg = _build_image_config(base_config, api_key)
    prompts_cfg = _build_prompts_config(persona_prompts)
    db_cfg = _build_database_config(base_config, grandma_cfg.name)

    config = Config(
        grandma=grandma_cfg,
        llm=llm_cfg,
        image=image_cfg,
        prompts=prompts_cfg,
        database=db_cfg,
    )

    logger.debug("Configuration loaded successfully: %s", config)
    return config


# -------------------------
# Utilities
# -------------------------
def list_personas(config_dir: str = DEFAULT_CONFIG_DIR) -> List[str]:
    """Return available persona file names (without extension)."""
    p = Path(config_dir) / PERSONAS_DIR
    if not p.exists():
        return []
    return [fp.stem for fp in p.glob("*.yaml") if fp.is_file()]

