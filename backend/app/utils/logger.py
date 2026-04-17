import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
LOG_FILE = os.path.join(LOG_DIR, "friday.log")

os.makedirs(LOG_DIR, exist_ok=True)

# Create logger
logger = logging.getLogger("FRIDAY")
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_fmt = logging.Formatter("%(asctime)s │ %(levelname)-7s │ %(message)s", datefmt="%H:%M:%S")
console_handler.setFormatter(console_fmt)

# File handler
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_fmt = logging.Formatter("%(asctime)s │ %(levelname)-7s │ %(name)s │ %(message)s")
file_handler.setFormatter(file_fmt)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def log_command(command: str, response: str):
    """Log a command-response pair."""
    logger.info(f"CMD: {command} → {response}")


def log_error(context: str, error: Exception):
    """Log an error with context."""
    logger.error(f"{context}: {error}")
