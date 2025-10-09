import logging
import pytest
from AntonIA.common.logger_setup import setup_logging

def test_setup_logging_returns_logger_instance():
    logger = setup_logging()
    assert isinstance(logger, logging.Logger)
    assert logger.name == "AntonIA"

def test_setup_logging_sets_logging_level(monkeypatch):
    # Reset logging configuration before test
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    setup_logging()
    assert logging.getLogger().level == logging.INFO

def test_logger_format(monkeypatch, caplog):
    setup_logging()
    logger = logging.getLogger("AntonIA")
    with caplog.at_level(logging.INFO):
        logger.info("Test message")
    # Check that the log message contains the expected format parts
    log_record = caplog.records[0]
    assert "AntonIA" in log_record.name
    assert log_record.levelname == "INFO"
    assert "Test message" in log_record.getMessage()