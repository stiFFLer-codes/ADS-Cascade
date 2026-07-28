"""
utils/logger.py
---------------
Centralised logging factory for the contai-analysis pipeline.
"""

import logging
from pathlib import Path

from config.settings import LOGS_DIR, LOG_LEVEL_FILE, LOG_LEVEL_CONSOLE

_FMT      = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str, log_file: str | None = None) -> logging.Logger:
    """
    Return a named logger with a console handler and an optional file handler.

    Parameters
    ----------
    name:     Logger name (typically the script stem, e.g. '01_company_inventory').
    log_file: If given, a file handler writing to ``LOGS_DIR / log_file`` is added.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if called more than once
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(_FMT, datefmt=_DATE_FMT)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, LOG_LEVEL_CONSOLE, logging.INFO))
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler (optional)
    if log_file:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(LOGS_DIR / log_file, encoding="utf-8")
        fh.setLevel(getattr(logging, LOG_LEVEL_FILE, logging.DEBUG))
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
