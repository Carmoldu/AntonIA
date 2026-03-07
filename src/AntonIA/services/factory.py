"""Service factory helpers for constructing client instances based on configuration.

This module is responsible for reading the configuration objects created by
Hydra (or tests) and instantiating the concrete implementation of each
interface (LLMClient, ImageGenerationClient, StorageClient, DatabaseClient).

The caller can pass additional contextual information (e.g. system prompt)
which is not stored in the config objects themselves.
"""
from __future__ import annotations

import os
from typing import Optional

from AntonIA.common import config as cfg_module
from AntonIA.services import (
    MockAIClient,
    OpenAIClient,
    MockImageGenerationClient,
    OpenAIimageGenerationClient,
    LocalStorageClient,
    AzureBlobStorageClient,
    MockStorageClient,
    LocalFileDatabaseClient,
    MockDatabaseClient,
)


# ---- llm ---------------------------------------------------------------
def create_llm_client(llm_cfg: cfg_module.LLMConfig, *, system_prompt: str = ""):
    """Return an LLM client based on configuration.

    Parameters
    ----------
    llm_cfg: LLMConfig
        The configuration dataclass or OmegaConf object for the LLM.
    system_prompt: str, optional
        A system prompt to supply when constructing an OpenAI client.

    Raises
    ------
    ValueError
        If the ``llm_cfg.type`` is not recognized.
    """
    t = getattr(llm_cfg, "type", "openai")
    if t == "openai":
        return OpenAIClient(
            api_key=llm_cfg.api_key,
            model=llm_cfg.model,
            system_prompt=system_prompt,
        )
    elif t == "mock":
        # mock ignores the api key/model values
        return MockAIClient(llm_cfg.response)
    else:
        raise ValueError(f"Unknown llm client type '{t}'")


# ---- image generation -------------------------------------------------
def create_image_client(img_cfg: cfg_module.ImageConfig):
    t = getattr(img_cfg, "type", "openai")
    if t == "openai":
        return OpenAIimageGenerationClient(api_key=img_cfg.api_key, model=img_cfg.model)
    elif t == "mock":
        return MockImageGenerationClient()
    else:
        raise ValueError(f"Unknown image generation client type '{t}'")


# ---- storage -----------------------------------------------------------
def create_storage_client(storage_cfg: cfg_module.StorageConfig):
    """Instantiate a storage client according to configuration."""
    t = getattr(storage_cfg, "type", "local")
    if t == "local":
        # for convenience allow the base_dir to be picked up from image config
        return LocalStorageClient(base_dir=storage_cfg.base_dir)
    elif t == "azure":
        conn = storage_cfg.connection_string or os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container = storage_cfg.container_name or os.getenv("AZURE_STORAGE_CONTAINER")
        return AzureBlobStorageClient(
            connection_string=conn,
            container_name=container,
            base_dir=storage_cfg.base_dir,
        )
    elif t == "mock":
        return MockStorageClient()
    else:
        raise ValueError(f"Unknown storage client type '{t}'")


# ---- database ----------------------------------------------------------
def create_database_client(db_cfg: cfg_module.DatabaseConfig):
    t = getattr(db_cfg, "type", "local")
    if t == "local":
        # expects a path to directory where parquet tables are stored
        return LocalFileDatabaseClient(db_path=db_cfg.past_records_path)
    elif t == "mock":
        return MockDatabaseClient()
    else:
        raise ValueError(f"Unknown database client type '{t}'")
