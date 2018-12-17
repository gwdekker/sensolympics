import logging
import pathlib

import dotenv


this_dir = pathlib.Path(__file__).resolve().parent
parent_dir = this_dir.parent


def get_logger():
    logger = logging.getLogger("Awesome Vang Disruption")
    logger.propagate = False
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # logger.setLevel(logging.DEBUG)
    return logger


def set_log_level(level):
    levels = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "warn": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }
    if not level:
        return
    if isinstance(level, str):
        level = levels[level.lower()]
    logging.getLogger().setLevel(level)


def load_dotenv():
    dotenv.load_dotenv(dotenv_path=this_dir / ".env")
