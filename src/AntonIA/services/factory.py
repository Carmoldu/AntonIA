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
    if llm_cfg.type == "open_ai":
        return OpenAIClient(
            api_key=llm_cfg.open_ai.api_key,
            model=llm_cfg.open_ai.model,
            system_prompt=system_prompt,
        )
    elif llm_cfg.type == "mock":
        # mock ignores the api key/model values
        return MockAIClient(llm_cfg.mock.response)
    else:
        raise ValueError(f"Unknown llm client type '{llm_cfg.type}'")


# ---- image generation -------------------------------------------------
def create_image_client(img_cfg: cfg_module.ImageConfig):
    if img_cfg.type == "open_ai":
        return OpenAIimageGenerationClient(
            api_key=img_cfg.open_ai.api_key, 
            model=img_cfg.open_ai.model,
            )
    elif img_cfg.type == "mock":
        return MockImageGenerationClient()
    else:
        raise ValueError(f"Unknown image generation client type '{img_cfg.type}'")


# ---- storage -----------------------------------------------------------
def create_storage_client(storage_cfg: cfg_module.StorageConfig):
    """Instantiate a storage client according to configuration."""
    if storage_cfg.type == "local":
        return LocalStorageClient(base_dir=storage_cfg.local.base_dir)
    elif storage_cfg.type == "azure":
        return AzureBlobStorageClient(
            connection_string=storage_cfg.azure.connection_string,
            container_name=storage_cfg.azure.container_name ,
            base_dir=storage_cfg.azure.base_dir,
        )
    elif storage_cfg.type == "mock":
        return MockStorageClient()
    else:
        raise ValueError(f"Unknown storage client type '{storage_cfg.type}'")


# ---- database ----------------------------------------------------------
def create_database_client(db_cfg: cfg_module.DatabaseConfig):
    if db_cfg.type == "local":
        # expects a path to directory where parquet tables are stored
        return LocalFileDatabaseClient(db_path=db_cfg.local.past_records_path)
    elif db_cfg.type == "mock":
        return MockDatabaseClient()
    else:
        raise ValueError(f"Unknown database client type '{db_cfg.type}'")
