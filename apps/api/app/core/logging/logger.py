"""
Enterprise logger configuration.
"""

from __future__ import annotations

import logging

from app.core.logging.config import logging_config
from app.core.logging.formatter import StandardFormatter


def configure_logging() -> None:
    """Configure application logging."""

    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    root_logger.setLevel(logging_config.log_level)

    if logging_config.enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(StandardFormatter())
        root_logger.addHandler(console_handler)