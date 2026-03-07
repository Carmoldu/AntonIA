from __future__ import annotations

import os
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from hydra import initialize, compose
from hydra.core.config_store import ConfigStore
from omegaconf import OmegaConf, MissingMandatoryValue

logger = logging.getLogger(__name__)

# -------------------------
# Constants
# -------------------------
# DEFAULT_CONFIG_DIR = "./config"
# ENV_OPENAI_API_KEY = "OPENAI_API_KEY"

# -------------------------
# Exceptions / dataclasses
# -------------------------
class ConfigError(RuntimeError):
    """Raised when configuration loading/validation fails."""


@dataclass
class GrandmaConfig:
    name: str
    runs_table_name: str
    prompts: PromptsConfig
    language: str = "catalan"
    hashtags: str = "#bondia #alegria #amor"
    watermark_path: Optional[str] = None

@dataclass
class LLMConfig:
    api_key: str
    model: str = "gpt-4.1-nano"
    temperature: float = 0.8


@dataclass
class ImageConfig:
    api_key: str
    model: str = "gpt-image-1-mini"
    size: str = "1024x1024"
    storage_path: str = "./outputs/images"


@dataclass
class PromptsConfig:
    system: str
    creation_template: str
    image_template: str
    instagram_caption_template: str


@dataclass
class DatabaseConfig:
    past_records_path: str
    past_records_to_retrieve: int = 10


@dataclass
class Config:
    grandma: GrandmaConfig
    llm: LLMConfig
    image: ImageConfig
    database: DatabaseConfig


# register config with Hydra so the @hydra.main entrypoint can construct it
cs = ConfigStore.instance()
cs.store(name="base_config", node=Config)


# -------------------------
# Public API
# -------------------------
# def load_config(persona: Optional[str] = None, config_dir: str = DEFAULT_CONFIG_DIR) -> Config:
#     """Compose Hydra configuration from *config_dir* and return a Config object.

#     ``persona`` is translated into a ``personas=<name>`` override; if omitted
#     the default persona is used.
#     """

#     # load dotenv so env vars from a .env file are available during tests
#     from dotenv import load_dotenv

#     load_dotenv()

#     overrides: list[str] = []
#     if persona:
#         overrides.append(f"personas={persona}")

#     try:
#         with initialize(config_path=config_dir, job_name="load_config"):
#             cfg = compose(config_name="config", overrides=overrides)
#     except MissingMandatoryValue as exc:
#         raise ConfigError(str(exc))

#     cfg_dict = OmegaConf.to_container(cfg, resolve=True)

#     # environment variable takes precedence
#     api_key = os.getenv(ENV_OPENAI_API_KEY) or cfg_dict.get("llm", {}).get("api_key")
#     if not api_key:
#         raise ConfigError(f"{ENV_OPENAI_API_KEY} not found in environment or config.")
#     cfg_dict["llm"]["api_key"] = api_key

#     # move system prompt out of the prompts section
#     system_prompt = cfg_dict["prompts"].pop("system", "")

#     try:
#         return Config(
#             grandma=GrandmaConfig(**cfg_dict["grandma"]),
#             llm=LLMConfig(**cfg_dict["llm"], system_prompt=system_prompt),
#             image=ImageConfig(**cfg_dict["image"]),
#             prompts=PromptsConfig(**cfg_dict["prompts"]),
#             database=DatabaseConfig(**cfg_dict["database"]),
#         )
#     except TypeError as exc:  # missing fields / bad types
#         raise ConfigError(str(exc))


# def list_personas(config_dir: str = DEFAULT_CONFIG_DIR) -> List[str]:
#     """Return available persona filenames (without extension)."""
#     p = Path(config_dir) / "personas"
#     if not p.exists():
#         return []
#     return [fp.stem for fp in p.glob("*.yaml") if fp.is_file()]

