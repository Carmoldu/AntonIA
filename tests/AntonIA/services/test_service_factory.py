import os
import pytest

from AntonIA.common import config as cfg_module
from AntonIA.services import (
    OpenAIClient,
    MockAIClient,
    OpenAIimageGenerationClient,
    MockImageGenerationClient,
    LocalStorageClient,
    AzureBlobStorageClient,
    MockStorageClient,
    LocalFileDatabaseClient,
    MockDatabaseClient,
)
from AntonIA.services import factory


def test_create_llm_client_openai(monkeypatch):
    cfg = cfg_module.LLMConfig(type="openai", api_key="k", model="m", temperature=0.7)
    # patch OpenAIClient to avoid network calls
    monkeypatch.setattr(
        "AntonIA.services.factory.OpenAIClient",
        lambda **kwargs: "openai-client",
    )
    client = factory.create_llm_client(cfg, system_prompt="sys")
    assert client == "openai-client"


def test_create_llm_client_mock():
    cfg = cfg_module.LLMConfig(type="mock", api_key="", model="")
    client = factory.create_llm_client(cfg)
    assert isinstance(client, MockAIClient)


def test_create_llm_client_bad_type():
    cfg = cfg_module.LLMConfig(type="not-a-thing", api_key="", model="")
    with pytest.raises(ValueError):
        factory.create_llm_client(cfg)


def test_create_image_client_openai(monkeypatch):
    cfg = cfg_module.ImageConfig(type="openai", api_key="k", model="m")
    monkeypatch.setattr(
        "AntonIA.services.factory.OpenAIimageGenerationClient",
        lambda **kwargs: "img-client",
    )
    assert factory.create_image_client(cfg) == "img-client"


def test_create_image_client_mock():
    cfg = cfg_module.ImageConfig(type="mock", api_key="", model="")
    client = factory.create_image_client(cfg)
    assert isinstance(client, MockImageGenerationClient)


def test_create_storage_client_local(tmp_path):
    cfg = cfg_module.StorageConfig(type="local", base_dir=str(tmp_path))
    client = factory.create_storage_client(cfg)
    assert isinstance(client, LocalStorageClient)
    assert client.base_dir == tmp_path


def test_create_storage_client_mock():
    cfg = cfg_module.StorageConfig(type="mock")
    client = factory.create_storage_client(cfg)
    assert isinstance(client, MockStorageClient)


def test_create_storage_client_azure(monkeypatch):
    cfg = cfg_module.StorageConfig(type="azure", connection_string="conn", container_name="cont")
    # patch AzureBlobStorageClient so it doesn't validate connection string
    monkeypatch.setattr(
        "AntonIA.services.factory.AzureBlobStorageClient",
        lambda **kwargs: "azure-client",
    )
    client = factory.create_storage_client(cfg)
    assert client == "azure-client"


def test_create_storage_client_bad_type():
    cfg = cfg_module.StorageConfig(type="unknown")
    with pytest.raises(ValueError):
        factory.create_storage_client(cfg)


def test_create_database_client_local(tmp_path):
    cfg = cfg_module.DatabaseConfig(type="local", past_records_path=str(tmp_path))
    client = factory.create_database_client(cfg)
    assert isinstance(client, LocalFileDatabaseClient)


def test_create_database_client_mock():
    cfg = cfg_module.DatabaseConfig(type="mock")
    client = factory.create_database_client(cfg)
    assert isinstance(client, MockDatabaseClient)


def test_create_database_client_bad_type():
    cfg = cfg_module.DatabaseConfig(type="oops")
    with pytest.raises(ValueError):
        factory.create_database_client(cfg)
