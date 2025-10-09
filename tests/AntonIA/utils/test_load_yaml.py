import pytest
from pathlib import Path
from AntonIA.utils.load_yaml import load_yaml
import tempfile
import os

def test_load_yaml_returns_dict_for_valid_yaml():
    yaml_content = "key: value\nnumber: 42"
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".yaml") as tmp:
        tmp.write(yaml_content)
        tmp_path = Path(tmp.name)
    try:
        result = load_yaml(tmp_path)
        assert isinstance(result, dict)
        assert result["key"] == "value"
        assert result["number"] == 42
    finally:
        os.remove(tmp_path)

def test_load_yaml_returns_empty_dict_for_missing_file():
    non_existent_path = Path("non_existent_file.yaml")
    result = load_yaml(non_existent_path)
    assert result == {}

def test_load_yaml_handles_empty_file():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".yaml") as tmp:
        tmp_path = Path(tmp.name)
    try:
        result = load_yaml(tmp_path)
        assert result is None or result == {}
    finally:
        os.remove(tmp_path)