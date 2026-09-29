from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

AccessRequestStatus = Literal[
    "pending",
    "reviewed",
    "contacted",
    "interview",
    "qualified",
    "report",
    "paid",
    "converted",
    "rejected",
]


class AccessRequestCreate(BaseModel):
    """Payload for requesting AIIP early access."""

    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    profile: str = Field(min_length=1, max_length=50)
    challenge: str = Field(min_length=1)
    consent: Literal[True]


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


class OperationsAccessRequestResponse(BaseModel):
    """Internal operations representation of an early-access request."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    profile: str
    challenge: str
    consent: bool
    status: AccessRequestStatus
    created_at: datetime
    updated_at: datetime


class AccessRequestStatusUpdate(BaseModel):
    """Payload for changing an early-access request's operational status."""

    status: AccessRequestStatus
