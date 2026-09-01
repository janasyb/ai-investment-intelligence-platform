from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AccessRequestCreate(BaseModel):
    """Payload for requesting AIIP early access."""

    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    profile: str = Field(min_length=1, max_length=50)
    challenge: str = Field(min_length=1)
    consent: bool


class AccessRequestResponse(BaseModel):
    """Public representation of an early-access request."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    profile: str
    challenge: str
    consent: bool
    status: str
    created_at: datetime
    updated_at: datetime
