"""
Environment definitions for AIIP Technologies.

This module defines the supported runtime environments for the
platform. These values are used throughout the application instead
of hard-coded strings.
"""

from enum import StrEnum


class Environment(StrEnum):
    """Supported application environments."""

    DEVELOPMENT = "development"
    LOCAL = "local"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

    @property
    def is_local(self) -> bool:
        return self in {
            Environment.LOCAL,
            Environment.DEVELOPMENT,
        }

    @property
    def is_testing(self) -> bool:
        return self is Environment.TESTING

    @property
    def is_staging(self) -> bool:
        return self is Environment.STAGING

    @property
    def is_production(self) -> bool:
        return self is Environment.PRODUCTION