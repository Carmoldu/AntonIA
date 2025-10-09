import pytest
from AntonIA.pipeline import main

@pytest.fixture
def mock_dependencies(monkeypatch):
    # Mock all external dependencies used in main
    monkeypatch.setattr("AntonIA.common.logger_setup.setup_logging", lambda: None)
    monkeypatch.setattr("AntonIA.common.config.load_config", lambda persona: type("Config", (), {
        "llm": type("LLM", (), {
            "api_key": "test_key",
            "model": "test_model",
            "system_prompt": "test_prompt",
            "temperature": 0.5
        })(),
        "image": type("Image", (), {
            "api_key": "img_key",
            "model": "img_model",
            "size": "512x512",
            "storage_path": "/tmp"
        })(),
        "database": type("Database", (), {
            "past_records_path": "/tmp/db",
            "runs_table_name": "runs",
            "past_records_to_retrieve": 1
        })(),
        "grandma": type("Grandma", (), {
            "language": "en",
            "watermark_path": "/tmp/watermark.png",
            "hashtags": "#test"
        })(),
        "prompts": type("Prompts", (), {
            "creation_template": "create_template",
            "image_gen_template": "image_gen_template",
            "instagram_caption_template": "caption_template"
        })()
    })())

    monkeypatch.setattr("AntonIA.services.OpenAIClient", lambda **kwargs: "llm_client")
    monkeypatch.setattr("AntonIA.services.OpenAIimageGenerationClient", lambda **kwargs: "image_client")
    monkeypatch.setattr("AntonIA.services.LocalStorageClient", lambda **kwargs: "storage_client")
    monkeypatch.setattr("AntonIA.services.LocalFileDatabaseClient", lambda **kwargs: "db_client")
    monkeypatch.setattr("AntonIA.utils.prompts.build_prompt_from_template", lambda template, ctx: "system_prompt")
    monkeypatch.setattr("AntonIA.core.retrieve_past_records.retrieve_past_n_days", lambda **kwargs: [])
    monkeypatch.setattr("AntonIA.core.prompt_generator.generate", lambda **kwargs: ("image_prompt", {
        "phrase": "Hello",
        "topic": "World",
        "style": "Modern",
        "font": "Arial"
    }))
    monkeypatch.setattr("AntonIA.core.instagram_caption_generator.generate", lambda *args, **kwargs: "Test caption")
    monkeypatch.setattr("AntonIA.core.image_generator.generate", lambda *args, **kwargs: b"image_bytes")
    monkeypatch.setattr("AntonIA.utils.image_utils.add_watermark_fn_factory", lambda *args, **kwargs: lambda img: img)
    monkeypatch.setattr("AntonIA.core.image_saver.save", lambda img_bytes, storage_client: "/tmp/image.png")
    monkeypatch.setattr("AntonIA.core.run_info_saver.RunInfo.from_generation_details", lambda **kwargs: "run_info")
    monkeypatch.setattr("AntonIA.core.run_info_saver.save", lambda db_client, table, run_info: None)

def test_main_runs_without_error(mock_dependencies):
    # Should not raise any exceptions
    main("test_persona")