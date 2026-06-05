"""ml_data v2/v3 columns

Revision ID: d4e5f6a7b8c9
Revises: c8d9e0f1a2b3
Create Date: 2026-06-05

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, Sequence[str], None] = "c8d9e0f1a2b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "audio_features",
        sa.Column(
            "processing_status",
            sa.String(length=30),
            server_default="pending",
            nullable=False,
        ),
    )
    op.add_column("audio_features", sa.Column("error_message", sa.Text(), nullable=True))
    op.add_column(
        "audio_features",
        sa.Column("predicted_visual_style", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column("predicted_color_palette", postgresql.ARRAY(sa.String()), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column("visual_embedding", postgresql.ARRAY(sa.Float()), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column("model_version", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column("inferred_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column("visual_motion_intensity", sa.Float(), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column("visual_texture_type", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column("visual_color_temperature", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column("visual_rhythm_sync", sa.Float(), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column(
            "genre_to_visual_mapping",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )
    op.add_column(
        "audio_features",
        sa.Column(
            "mood_to_color_mapping",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )
    op.add_column(
        "audio_features",
        sa.Column("beat_timestamps", postgresql.ARRAY(sa.Float()), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column("highlight_start_sec", sa.Float(), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column("highlight_end_sec", sa.Float(), nullable=True),
    )
    op.add_column(
        "audio_features",
        sa.Column("onset_strength", sa.Float(), nullable=True),
    )

    op.add_column(
        "generation_logs",
        sa.Column("target_platform", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "generation_logs",
        sa.Column("aspect_ratio", sa.String(length=10), nullable=True),
    )
    op.add_column(
        "generation_logs",
        sa.Column("target_duration_sec", sa.Float(), nullable=True),
    )
    op.add_column(
        "generation_logs",
        sa.Column("loop_duration_sec", sa.Float(), nullable=True),
    )
    op.add_column(
        "generation_logs",
        sa.Column("loop_beat_aligned", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "generation_logs",
        sa.Column("frame_rate", sa.Integer(), nullable=True),
    )
    op.add_column(
        "generation_logs",
        sa.Column("loop_sync_offset_ms", sa.Integer(), nullable=True),
    )

    op.add_column(
        "visual_ratings",
        sa.Column("platform", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "visual_ratings",
        sa.Column("loop_smoothness_score", sa.Integer(), nullable=True),
    )
    op.add_column(
        "visual_ratings",
        sa.Column("beat_sync_score", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("visual_ratings", "beat_sync_score")
    op.drop_column("visual_ratings", "loop_smoothness_score")
    op.drop_column("visual_ratings", "platform")

    op.drop_column("generation_logs", "loop_sync_offset_ms")
    op.drop_column("generation_logs", "frame_rate")
    op.drop_column("generation_logs", "loop_beat_aligned")
    op.drop_column("generation_logs", "loop_duration_sec")
    op.drop_column("generation_logs", "target_duration_sec")
    op.drop_column("generation_logs", "aspect_ratio")
    op.drop_column("generation_logs", "target_platform")

    op.drop_column("audio_features", "onset_strength")
    op.drop_column("audio_features", "highlight_end_sec")
    op.drop_column("audio_features", "highlight_start_sec")
    op.drop_column("audio_features", "beat_timestamps")
    op.drop_column("audio_features", "mood_to_color_mapping")
    op.drop_column("audio_features", "genre_to_visual_mapping")
    op.drop_column("audio_features", "visual_rhythm_sync")
    op.drop_column("audio_features", "visual_color_temperature")
    op.drop_column("audio_features", "visual_texture_type")
    op.drop_column("audio_features", "visual_motion_intensity")
    op.drop_column("audio_features", "inferred_at")
    op.drop_column("audio_features", "model_version")
    op.drop_column("audio_features", "visual_embedding")
    op.drop_column("audio_features", "predicted_color_palette")
    op.drop_column("audio_features", "predicted_visual_style")
    op.drop_column("audio_features", "error_message")
    op.drop_column("audio_features", "processing_status")
