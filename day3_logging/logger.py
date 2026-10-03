import json
import logging
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs log records as a JSON string."""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "function": record.funcName,
            "message": record.getMessage(),
        }
        return json.dumps(log_entry)


def setup_logger():
    """Configures and returns a logger with the JSON formatter."""
    logger = logging.getLogger("agent-foundry")
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if setup is called more than once
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    return logger


# Initialize the logger
logger = setup_logger()


def perform_operation(success: bool):
    """Simulates an operation that can succeed or fail, and logs the result."""
    if success:
        logger.info("Database connection established successfully.")
    else:
        logger.error("Failed to connect to the database: timeout.")


if __name__ == "__main__":
    print("--- Testing Success Outcome ---")
    perform_operation(success=True)

    print("\n--- Testing Failure Outcome ---")
    perform_operation(success=False)