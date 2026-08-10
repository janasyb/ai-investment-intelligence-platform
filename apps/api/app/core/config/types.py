"""
Reusable type aliases for configuration.
"""

from typing import Annotated

from pydantic import Field

Port = Annotated[int, Field(ge=1, le=65535)]

PositiveInt = Annotated[int, Field(gt=0)]

NonEmptyString = Annotated[str, Field(min_length=1)]