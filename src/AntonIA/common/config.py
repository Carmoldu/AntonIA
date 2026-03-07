from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, Any

from hydra.core.config_store import ConfigStore

logger = logging.getLogger(__name__)



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
class PromptsConfig:
    system: str
    creation_template: str
    image_template: str
    instagram_caption_template: str


@dataclass
class OpenAILLMConfig:
    type: str = "gpt-4.1"
    api_key: str = ""
    model: str = "gpt-4.1"
    temperature: float = 0.8

@dataclass
class MockLLMConfig:
    type: str = "mock"
    response: str = '{"phrase": "Good Morning", "topic": "Nice sunset", "style": "Aquarela", "font": "Comic Sans"}'
    temperature: float = 0.8

@dataclass
class OpenAIImageConfig:
    type: str = "openai"
    api_key: str = ""
    model: str = "gpt-image-1-mini"
    size: str = "1024x1024"
    storage_path: str = "./outputs/images"

@dataclass
class MockImageConfig:
    type: str = "mock"
    size: str = "1024x1024"


@dataclass
class LocalDatabaseConfig:
    type: str = "local"
    past_records_path: str = ""

@dataclass
class MockDatabaseConfig:
    type: str = "mock"


@dataclass
class AzureStorageConfig:
    type: str = "local"
    base_dir: str | None = None
    connection_string: str | None = None
    container_name: str | None = None

@dataclass
class LocalStorageConfig:
    type: str = "local"
    base_dir: str = "./outputs/storage"

@dataclass
class MockStorageConfig:
    type: str = "mock"


# @dataclass
# class Config:
#     grandma: GrandmaConfig
#     llm: OpenAILLMConfig | MockLLMConfig
#     image: OpenAIImageConfig | MockImageConfig
#     storage: AzureStorageConfig | LocalStorageConfig | MockStorageConfig
#     database: LocalDatabaseConfig | MockDatabaseConfig


@dataclass
class Config:
    grandma: GrandmaConfig
    llm: Any
    image: Any
    storage: Any
    database: Any
    past_records_to_retrieve: int = 10


# register config with Hydra so the @hydra.main entrypoint can construct it
cs = ConfigStore.instance()
cs.store(name="base_config", node=Config)
cs.store(group="llm", name="mock", node=MockLLMConfig)
cs.store(group="image", name="openai", node=OpenAIImageConfig)
cs.store(group="image", name="mock", node=MockImageConfig)
cs.store(group="storage", name="local", node=LocalStorageConfig)
cs.store(group="llm", name="openai", node=OpenAILLMConfig)
cs.store(group="storage", name="azure", node=AzureStorageConfig)
cs.store(group="storage", name="mock", node=MockStorageConfig)
cs.store(group="database", name="local", node=LocalDatabaseConfig)
cs.store(group="database", name="mock", node=MockDatabaseConfig)

