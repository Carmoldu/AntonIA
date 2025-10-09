import pytest
from datetime import datetime
from AntonIA.core.run_info_saver import RunInfo, save

class DummyDBClient:
    def __init__(self):
        self.saved = []

    def save_record(self, table, record):
        self.saved.append((table, record))

def test_runinfo_as_dict():
    run_info = RunInfo(
        prompt="Test prompt",
        phrase="Test phrase",
        topic="Test topic",
        style="Test style",
        caption="Test caption",
        image_path="/tmp/image.png"
    )
    d = run_info.as_dict()
    assert d["prompt"] == "Test prompt"
    assert d["phrase"] == "Test phrase"
    assert d["topic"] == "Test topic"
    assert d["style"] == "Test style"
    assert d["caption"] == "Test caption"
    assert d["image_path"] == "/tmp/image.png"
    assert isinstance(d["timestamp"], datetime)

def test_runinfo_from_generation_details():
    prompt = "Prompt"
    response_details = {
        "phrase": "Phrase",
        "topic": "Topic",
        "style": "Style"
    }
    caption = "Caption"
    image_path = "/img.png"
    run_info = RunInfo.from_generation_details(prompt, response_details, caption, image_path)
    assert run_info.prompt == prompt
    assert run_info.phrase == "Phrase"
    assert run_info.topic == "Topic"
    assert run_info.style == "Style"
    assert run_info.caption == caption
    assert run_info.image_path == image_path

def test_save_calls_dbclient(monkeypatch):
    db_client = DummyDBClient()
    run_info = RunInfo(
        prompt="Prompt",
        phrase="Phrase",
        topic="Topic",
        style="Style",
        caption="Caption",
        image_path="/img.png"
    )
    save(db_client, "runs", run_info)
    assert db_client.saved
    table, record = db_client.saved[0]
    assert table == "runs"
    assert record["prompt"] == "Prompt"
    assert record["phrase"] == "Phrase"
    assert record["topic"] == "Topic"
    assert record["style"] == "Style"
    assert record["caption"] == "Caption"
    assert record["image_path"] == "/img.png"
    assert isinstance(record["timestamp"], datetime)