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
    temperature_for_image_prompt_generation: float = 0.8
    temperature_for_caption_generation: float = 0.8
    publishers: Optional[list[PublisherConfig]] = None

@dataclass
class PromptsConfig:
    system: str
    creation_template: str
    image_template: str
    instagram_caption_template: str


@dataclass
class PublisherConfig:
    type: str
    instagram: Optional[InstagramPublisherConfig] = None
    whatsapp: Optional[None] = None  # Placeholder for future WhatsApp config


@dataclass
class InstagramPublisherConfig:
    access_token: str
    instagram_account_id: str
    base_image_url: str




@dataclass
class LLMConfig:
    open_ai: OpenAILLMConfig
    mock: MockLLMConfig
    type: str = "mock"

@dataclass
class OpenAILLMConfig:
    api_key: str = ""
    model: str = "gpt-4.1"
    temperature: float = 0.8

@dataclass
class MockLLMConfig:
    response: str = '{"phrase": "Good Morning", "topic": "Nice sunset", "style": "Aquarela", "font": "Comic Sans"}'
    temperature: float = 0.3


@dataclass
class ImageConfig:
    open_ai: OpenAIImageConfig
    size: str = "1024x1024"
    type: str = "mock"
    storage_path: str = "./outputs/images"

# Note ImageConfig does not have a Mock because the mock image client does not require 
# any configuration, but we could easily add one if needed in the future

@dataclass
class OpenAIImageConfig:
    api_key: str = ""
    model: str = "gpt-image-1-mini"


@dataclass
class DatabaseConfig:
    local: LocalDatabaseConfig
    type: str = "mock"

# Note DatabaseConfig does not have a Mock because the mock database client does not require 
# any configuration, but we could easily add one if needed in the future


@dataclass
class LocalDatabaseConfig:
    type: str = "local"
    past_records_path: str = ""


@dataclass
class StorageConfig:
    local: LocalStorageConfig
    azure: AzureStorageConfig
    type: str = "mock"


# Note StorageConfig does not have a Mock because the mock storage client does not require 
# any configuration, but we could easily add one if needed in the future

@dataclass
class AzureStorageConfig:
    type: str = "local"
    url: str = ""
    base_dir: str | None = None
    connection_string: str | None = None
    container_name: str | None = None

@dataclass
class LocalStorageConfig:
    type: str = "local"
    base_dir: str = "./outputs/storage"


@dataclass
class ProfileConfig:
    llm: str = "mock"
    image: str = "mock"
    storage: str = "mock"
    database: str = "mock"

@dataclass
class Config:
    grandma: GrandmaConfig
    llm: LLMConfig
    image: ImageConfig
    storage: StorageConfig
    database: DatabaseConfig
    profile: ProfileConfig
    past_records_to_retrieve: int = 10


# register config with Hydra so the @hydra.main entrypoint can construct it
cs = ConfigStore.instance()
cs.store(name="base_config", node=Config)

