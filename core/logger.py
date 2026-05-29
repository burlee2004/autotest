import logging
import sys
from pathlib import Path

BASE_LOGGER_NAME = "automation_framework"
DEFAULT_LOG_FILE = "reports/logs/framework.log"


def _configure_base_logger(level=logging.INFO, log_to_file=True, log_file=DEFAULT_LOG_FILE):
    logger = logging.getLogger(BASE_LOGGER_NAME)

    if getattr(logger, "_is_configured", False):
        return logger

    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-5s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_to_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger._is_configured = True
    return logger


def get_logger(name=None, level=logging.INFO, log_to_file=True, log_file=DEFAULT_LOG_FILE):
    base_logger = _configure_base_logger(
        level=level,
        log_to_file=log_to_file,
        log_file=log_file,
    )

    if name:
        return base_logger.getChild(name)

    return base_logger