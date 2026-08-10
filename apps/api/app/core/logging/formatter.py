"""
Logging formatter definitions.
"""

from __future__ import annotations

import logging

from app.core.logging.config import logging_config


class StandardFormatter(logging.Formatter):
    """Default formatter used throughout AIIP."""

    def __init__(self) -> None:
        super().__init__(
            fmt=logging_config.log_format,
            datefmt=logging_config.date_format,
        )