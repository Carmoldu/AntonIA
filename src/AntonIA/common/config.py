from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import yaml



@dataclass
class Config:
    grandma_name:str
    runs_table_name: str
    openai_api_key: str
    llm_model: str
    llm_temperature: float
    llm_system_prompt: str
    prompt_creation_template: str
    image_prompt_template: str
    instagram_caption_template: str
    image_model: str
    image_size: str
    image_storage_path: str
    past_records_database_path: str
    past_records_to_retrieve: int
    watermark_path: Optional[str]

    @classmethod
    def from_sources(cls, config_path: str = "./config.yaml") -> Config:
        """
        Initialize configuration from YAML file and environment variables.
        Environment variables take precedence.
        """
        # 1. Load .env file if present
        load_dotenv()

        # 2. Load YAML config (if exists)
        yaml_data = {}
        path = Path(config_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f) or {}

        # Compose some of the configs
        runs_table_name = f"{yaml_data['GRANDMA_NAME']}_runs"

        # 3. Merge environment variables (override YAML)
        merged = {
            "grandma_name": yaml_data["GRANDMA_NAME"],
            "runs_table_name": runs_table_name,
            "openai_api_key": os.getenv("OPENAI_API_KEY", None),
            "llm_model": yaml_data.get("LLM_MODEL", "gpt-4.1-nano"),
            "llm_temperature": float(yaml_data.get("LLM_TEMPERATURE", 0.8)),
            "llm_system_prompt": yaml_data.get("LLM_SYSTEM_PROMPT", ""),
            "prompt_creation_template": yaml_data["PROMPT_CREATION_TEMPLATE"],
            "image_prompt_template": yaml_data["IMAGE_PROMPT_TEMPLATE"],
            "instagram_caption_template": yaml_data["INSTAGRAM_CAPTION_TEMPLATE"],
            "image_model": yaml_data.get("IMAGE_MODEL", "gpt-image-1"),
            "image_size": yaml_data.get("IMAGE_SIZE", "1024x1024"),
            "image_storage_path": yaml_data.get("IMAGE_STORAGE_PATH", "./outputs/images"),
            "past_records_database_path": yaml_data["PAST_RECORDS_DATABASE_PATH"],
            "past_records_to_retrieve": yaml_data.get("PAST_RECORDS_TO_RETRIEVE", 10),
            "watermark_path": yaml_data.get("WATERMARK_PATH", None),
        }

        # 4. Validate critical fields
        if not merged["openai_api_key"]:
            raise ValueError("OPENAI_API_KEY not found in environment or config file.")

        return cls(**merged)


config = Config.from_sources()
