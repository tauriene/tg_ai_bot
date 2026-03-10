import logging
import pathlib

from logging.handlers import RotatingFileHandler
from bot.utils import config


def setup_logging(filename: str) -> None:
    log_dir = pathlib.Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO if config.debug else logging.WARNING)

    file_handler = RotatingFileHandler(
        log_dir / filename, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - [%(levelname)s] - %(name)s - "
            "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
        )
    )

    logger.addHandler(file_handler)
