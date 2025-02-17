import logging
from pathlib import Path

BASE_PROJECT_DIR = Path(__file__).parent.parent
LOGS_DIR = "logs"
LOGS_FILE_NAME = "app.log"
LOGGING_LEVEL = logging.DEBUG

logs_dir = BASE_PROJECT_DIR / LOGS_DIR

if not (logs_dir.exists() and logs_dir.is_dir()):
    logs_dir.mkdir()

LOG_FILE = Path(LOGS_DIR) / LOGS_FILE_NAME

logger = logging.getLogger("slava_s_bank_app")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s"
)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)
file_handler.setLevel(LOGGING_LEVEL)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(LOGGING_LEVEL)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.propagate = False
