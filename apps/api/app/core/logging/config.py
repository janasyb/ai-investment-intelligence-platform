"""
Enterprise logging configuration.

This module centralizes all logging configuration values for AIIP.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass


@dataclass(frozen=True)
class LoggingConfig:
    """Immutable logging configuration."""

    service_name: str = "aiip-api"
    environment: str = "development"

    log_level: int = logging.INFO

    log_format: str = "%(asctime)s | " "%(levelname)-8s | " "%(name)s | " "%(message)s"

    date_format: str = "%Y-%m-%d %H:%M:%S"

    use_json: bool = False

    enable_console: bool = True

    enable_file: bool = False

    log_file: str = "logs/api.log"


logging_config = LoggingConfig()
