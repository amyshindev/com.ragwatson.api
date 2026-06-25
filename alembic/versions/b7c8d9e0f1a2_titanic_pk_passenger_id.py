"""titanic_pk_passenger_id

Revision ID: b7c8d9e0f1a2
Revises: a1b2c3d4e5f6
Create Date: 2026-06-04

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "b7c8d9e0f1a2"
down_revision: str | Sequence[str] | None = "a1b2c3d4e5f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_index("ix_titanic_bookings_person_id", table_name="titanic_bookings")
    op.drop_table("titanic_bookings")
    op.drop_table("titanic_persons")

    op.create_table(
        "titanic_persons",
        sa.Column("passenger_id", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("gender", sa.String(length=16), nullable=False),
        sa.Column("age", sa.String(length=16), nullable=False),
        sa.Column("sib_sp", sa.String(length=16), nullable=False),
        sa.Column("parch", sa.String(length=16), nullable=False),
        sa.Column("survived", sa.String(length=8), nullable=False),
        sa.PrimaryKeyConstraint("passenger_id"),
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


def downgrade() -> None:
    op.drop_table("titanic_bookings")
    op.drop_table("titanic_persons")

    op.create_table(
        "titanic_persons",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("passenger_id", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("gender", sa.String(length=16), nullable=False),
        sa.Column("age", sa.String(length=16), nullable=False),
        sa.Column("sib_sp", sa.String(length=16), nullable=False),
        sa.Column("parch", sa.String(length=16), nullable=False),
        sa.Column("survived", sa.String(length=8), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("passenger_id"),
    )

    op.create_table(
        "titanic_bookings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("person_id", sa.Integer(), nullable=False),
        sa.Column("pclass", sa.String(length=8), nullable=False),
        sa.Column("ticket", sa.String(length=64), nullable=False),
        sa.Column("fare", sa.String(length=32), nullable=False),
        sa.Column("cabin", sa.String(length=32), nullable=False),
        sa.Column("embarked", sa.String(length=8), nullable=False),
        sa.ForeignKeyConstraint(["person_id"], ["titanic_persons.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_titanic_bookings_person_id", "titanic_bookings", ["person_id"])
