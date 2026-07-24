import logging
from pathlib import Path


def setup_logger(config):
    """
    Configure and return the application logger.
    """

    log_dir = Path(
        config["logging"]["directory"]
    )

    log_file = log_dir / config["logging"]["file"]

    log_level = getattr(
        logging,
        config["logging"]["level"].upper(),
        logging.INFO
    )

    log_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger("SubEnum")

    logger.setLevel(log_level)

    # Prevent duplicate handlers if setup_logger() is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger