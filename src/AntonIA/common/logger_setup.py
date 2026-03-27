import logging
import sys
import io

def setup_logging():
    # Reconfigure both stdout and stderr to use UTF-8 with error replacement
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    
    # Create handler with explicit UTF-8 encoding to handle emoji and special chars
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    
    # Force UTF-8 encoding on the handler
    if hasattr(handler, "encoding"):
        handler.encoding = "utf-8"
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = []
    root_logger.addHandler(handler)

    # Suppress verbose Azure SDK logging
    logging.getLogger("azure.core.pipeline").setLevel(logging.WARNING)
    logging.getLogger("azure.storage.blob").setLevel(logging.WARNING)

    return logging.getLogger("AntonIA")