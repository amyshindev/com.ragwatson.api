"""add_ml_data_4_layers

Revision ID: f6af73a4f087
Revises:
Create Date: 2026-05-22 15:45:39.034469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f6af73a4f087"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "audio_features",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("workspace_id", sa.BigInteger(), nullable=True),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("bpm", sa.Float(), nullable=True),
        sa.Column("energy", sa.Float(), nullable=True),
        sa.Column("valence", sa.Float(), nullable=True),
        sa.Column("danceability", sa.Float(), nullable=True),
        sa.Column("spectral_centroid", sa.Float(), nullable=True),
        sa.Column("loudness", sa.Float(), nullable=True),
        sa.Column("key", sa.Integer(), nullable=True),
        sa.Column("mode", sa.Integer(), nullable=True),
        sa.Column("genre_primary", sa.String(length=100), nullable=True),
        sa.Column("genre_secondary", sa.String(length=100), nullable=True),
        sa.Column("mood_tags", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("source", sa.String(length=50), server_default="upload", nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("duration_sec", sa.Float(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["workspace_id"], ["studio_workspaces.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audio_features_user_id", "audio_features", ["user_id"])

    op.create_table(
        "user_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("session_id", sa.String(length=100), nullable=True),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("target_type", sa.String(length=50), nullable=True),
        sa.Column("dwell_ms", sa.Integer(), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_events_user_id", "user_events", ["user_id"])

    op.create_table(
        "generation_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("workspace_id", sa.BigInteger(), nullable=True),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("audio_feature_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("prompt_params", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("model_version", sa.String(length=100), nullable=True),
        sa.Column("pipeline_version", sa.String(length=50), nullable=True),
        sa.Column("output_asset_url", sa.Text(), nullable=True),
        sa.Column("render_ms", sa.Integer(), nullable=True),
        sa.Column("quality_score", sa.Float(), nullable=True),
        sa.Column("style_vector", postgresql.ARRAY(sa.Float()), nullable=True),
        sa.Column("status", sa.String(length=30), server_default="pending", nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["audio_feature_id"], ["audio_features.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["workspace_id"], ["studio_workspaces.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_generation_logs_user_id", "generation_logs", ["user_id"])

    op.create_table(
        "visual_ratings",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("generation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rater_id", sa.BigInteger(), nullable=False),
        sa.Column("aesthetic_score", sa.Integer(), nullable=True),
        sa.Column("genre_match_score", sa.Integer(), nullable=True),
        sa.Column("mood_match_score", sa.Integer(), nullable=True),
        sa.Column("ab_test_id", sa.String(length=100), nullable=True),
        sa.Column("ab_winner", sa.Boolean(), nullable=True),
        sa.Column("flag", sa.String(length=30), server_default="ok", nullable=False),
        sa.Column("flag_reason", sa.Text(), nullable=True),
        sa.Column("rater_type", sa.String(length=20), server_default="user", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["generation_id"], ["generation_logs.id"]),
        sa.ForeignKeyConstraint(["rater_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_visual_ratings_rater_id", "visual_ratings", ["rater_id"])


def downgrade() -> None:
    op.drop_index("ix_visual_ratings_rater_id", table_name="visual_ratings")
    op.drop_table("visual_ratings")
    op.drop_index("ix_generation_logs_user_id", table_name="generation_logs")
    op.drop_table("generation_logs")
    op.drop_index("ix_user_events_user_id", table_name="user_events")
    op.drop_table("user_events")
    op.drop_index("ix_audio_features_user_id", table_name="audio_features")
    op.drop_table("audio_features")
