# logger.py
import logging
import os
import sys
from datetime import datetime

_FORMAT = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"

_handlers = [logging.StreamHandler(sys.stdout)]

# File logging is a nice-to-have locally, but on some hosts (or read-only
# filesystems) writing to disk can fail. Never let that crash the app —
# console logging (captured by Render/most hosts automatically) always
# works regardless.
try:
    LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
    logs_path = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_path, exist_ok=True)
    LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)
    _handlers.append(logging.FileHandler(LOG_FILE_PATH))
except OSError:
    pass

logging.basicConfig(
    format=_FORMAT,
    level=logging.INFO,
    handlers=_handlers,
)

if __name__ == "__main__":
    logging.info("Logging has started")
