from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv
import yaml



@dataclass
class Config:
    openai_api_key: str
    model_name: str
    watermark_path: str

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

        # 3. Merge environment variables (override YAML)
        merged = {
            "openai_api_key": os.getenv("OPENAI_API_KEY", None),
            "model_name": yaml_data.get("MODEL_NAME", "gpt-5"),
            "watermark_path": yaml_data.get("WATERMARK_PATH", None),
        }

        # 4. Validate critical fields
        if not merged["openai_api_key"]:
            raise ValueError("OPENAI_API_KEY not found in environment or config file.")

        return cls(**merged)


config = Config.from_sources()
