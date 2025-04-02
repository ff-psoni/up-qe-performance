import datetime
import logging
import os

LOG_DIR = "reports"
os.makedirs(LOG_DIR, exist_ok=True)


# Log file to collect all logs in one file
log_file = f"{LOG_DIR}/performance_log_test_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"


def get_logger(name, on_console=True):
    logger = logging.getLogger(name)


    if not logger.hasHandlers():  # Avoid duplicate handlers
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

        # Console handler
        if on_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # File handler
        file_handler = logging.FileHandler(log_file, mode='a')  # Append mode
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
