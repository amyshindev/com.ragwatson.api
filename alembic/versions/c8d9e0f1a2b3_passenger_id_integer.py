"""passenger_id_integer

Revision ID: c8d9e0f1a2b3
Revises: b7c8d9e0f1a2
Create Date: 2026-06-04

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c8d9e0f1a2b3"
down_revision: Union[str, Sequence[str], None] = "b7c8d9e0f1a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("titanic_bookings")
    op.alter_column(
        "titanic_persons",
        "passenger_id",
        existing_type=sa.String(length=32),
        type_=sa.Integer(),
        postgresql_using="passenger_id::integer",
        existing_nullable=False,
    )

    op.create_table(
        "titanic_bookings",
        sa.Column("passenger_id", sa.Integer(), nullable=False),
        sa.Column("pclass", sa.String(length=8), nullable=False),
        sa.Column("ticket", sa.String(length=64), nullable=False),
        sa.Column("fare", sa.String(length=32), nullable=False),
        sa.Column("cabin", sa.String(length=32), nullable=False),
        sa.Column("embarked", sa.String(length=8), nullable=False),
        sa.ForeignKeyConstraint(
            ["passenger_id"],
            ["titanic_persons.passenger_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("passenger_id"),
    )


def downgrade() -> None:
    op.drop_table("titanic_bookings")
    op.alter_column(
        "titanic_persons",
        "passenger_id",
        existing_type=sa.Integer(),
        type_=sa.String(length=32),
        postgresql_using="passenger_id::text",
        existing_nullable=False,
    )

    op.create_table(
        "titanic_bookings",
        sa.Column("passenger_id", sa.String(length=32), nullable=False),
        sa.Column("pclass", sa.String(length=8), nullable=False),
        sa.Column("ticket", sa.String(length=64), nullable=False),
        sa.Column("fare", sa.String(length=32), nullable=False),
        sa.Column("cabin", sa.String(length=32), nullable=False),
        sa.Column("embarked", sa.String(length=8), nullable=False),
        sa.ForeignKeyConstraint(
            ["passenger_id"],
            ["titanic_persons.passenger_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("passenger_id"),
    )
