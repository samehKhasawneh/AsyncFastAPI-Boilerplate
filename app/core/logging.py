import sys
from loguru import logger
from pathlib import Path
from app.core.config import settings


LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / "app.log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()

log_level = settings.LOG_LEVEL.upper()

logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    level=log_level,
    backtrace=True,
    diagnose=True,
    enqueue=True
)

logger.add(
    LOG_FILE,
    level=log_level,
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    rotation="20 MB",
    retention="10 days",
    compression="zip",
    enqueue=True
)

