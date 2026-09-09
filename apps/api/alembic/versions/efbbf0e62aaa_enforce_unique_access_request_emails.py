"""Enforce unique access request emails.

Revision ID: efbbf0e62aaa
Revises: 8c68e00886a4
Create Date: 2026-09-04
"""

from collections.abc import Sequence

from alembic import op

revision: str = "efbbf0e62aaa"
down_revision: str | Sequence[str] | None = "8c68e00886a4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Enforce one access request per email address."""
    op.drop_index(
        op.f("ix_access_requests_email"),
        table_name="access_requests",
    )

    op.create_unique_constraint(
        "uq_access_requests_email",
        "access_requests",
        ["email"],
    )


def downgrade() -> None:
    """Restore the previous non-unique email index."""
    op.drop_constraint(
        "uq_access_requests_email",
        "access_requests",
        type_="unique",
    )

    op.create_index(
        op.f("ix_access_requests_email"),
        "access_requests",
        ["email"],
        unique=False,
    )
