import datetime

from loguru import logger
import sys
import os

LOG_DIR = "reports"
os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:SS} {level} {message}", level="INFO")
logger.add(f"{LOG_DIR}/performance_test_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",format="{time:YYYY-MM-DD HH:mm:SS} {level} {message}", rotation="10 MB", level="DEBUG")
