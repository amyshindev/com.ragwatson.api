import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.inbound.api.schemas.training_export import (
    DatasetStatsRead,
    TrainingRecord,
)
from audio.adapter.outbound.orm.audio_feature_orm import AudioFeature
from audio.adapter.outbound.orm.generation_log_orm import GenerationLog
from audio.adapter.outbound.orm.visual_rating_orm import VisualRating
from audio.app.ports.output.training_export_repository import TrainingExportRepository

logger = logging.getLogger(__name__)


class TrainingExportPgRepository(TrainingExportRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def export_labeled_dataset(
        self,
        min_aesthetic_score: int = 3,
        limit: int = 10000,
    ) -> list[TrainingRecord]:
        stmt = (
            select(AudioFeature, GenerationLog, VisualRating)
            .join(
                GenerationLog,
                GenerationLog.audio_feature_id == AudioFeature.id,
            )
            .join(
                VisualRating,
                VisualRating.generation_id == GenerationLog.id,
            )
            .where(VisualRating.aesthetic_score >= min_aesthetic_score)
            .where(AudioFeature.processing_status == "done")
            .where(GenerationLog.status == "completed")
            .order_by(VisualRating.created_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        records: list[TrainingRecord] = []
        for af, gl, vr in result.all():
            records.append(
                TrainingRecord(
                    audio_feature_id=af.id,
                    bpm=af.bpm,
                    energy=af.energy,
                    valence=af.valence,
                    danceability=af.danceability,
                    spectral_centroid=af.spectral_centroid,
                    loudness=af.loudness,
                    genre_primary=af.genre_primary,
                    mood_tags=af.mood_tags,
                    beat_timestamps=af.beat_timestamps,
                    highlight_start_sec=af.highlight_start_sec,
                    highlight_end_sec=af.highlight_end_sec,
                    onset_strength=af.onset_strength,
                    visual_motion_intensity=af.visual_motion_intensity,
                    visual_texture_type=af.visual_texture_type,
                    visual_color_temperature=af.visual_color_temperature,
                    visual_rhythm_sync=af.visual_rhythm_sync,
                    genre_to_visual_mapping=af.genre_to_visual_mapping,
                    mood_to_color_mapping=af.mood_to_color_mapping,
                    predicted_visual_style=af.predicted_visual_style,
                    predicted_color_palette=af.predicted_color_palette,
                    visual_embedding=af.visual_embedding,
                    prompt_params=gl.prompt_params,
                    model_version=gl.model_version,
                    target_platform=gl.target_platform,
                    loop_duration_sec=gl.loop_duration_sec,
                    loop_beat_aligned=gl.loop_beat_aligned,
                    frame_rate=gl.frame_rate,
                    aesthetic_score=vr.aesthetic_score,
                    genre_match_score=vr.genre_match_score,
                    mood_match_score=vr.mood_match_score,
                    loop_smoothness_score=vr.loop_smoothness_score,
                    beat_sync_score=vr.beat_sync_score,
                    platform_rated=vr.platform,
                    ab_winner=vr.ab_winner,
                )
            )
        logger.info("[TrainingExportPgRepository] export count=%s", len(records))
        return records

    async def get_dataset_stats(self) -> DatasetStatsRead:
        af_count = await self._session.scalar(select(func.count(AudioFeature.id)))
        gl_count = await self._session.scalar(select(func.count(GenerationLog.id)))
        vr_count = await self._session.scalar(select(func.count(VisualRating.id)))

        avg_result = await self._session.execute(
            select(
                func.avg(VisualRating.aesthetic_score),
                func.avg(VisualRating.loop_smoothness_score),
                func.avg(VisualRating.beat_sync_score),
            )
        )
        avg_aesthetic, avg_loop, avg_sync = avg_result.one()

        labeled = await self._session.scalar(
            select(func.count(VisualRating.id)).where(VisualRating.aesthetic_score >= 3)
        )

        platform_result = await self._session.execute(
            select(
                GenerationLog.target_platform,
                func.count(GenerationLog.id),
            ).group_by(GenerationLog.target_platform)
        )
        platform_breakdown: dict[str, int] = {}
        for platform, count in platform_result.all():
            key = platform or "unknown"
            platform_breakdown[key] = int(count or 0)

        return DatasetStatsRead(
            total_audio_features=int(af_count or 0),
            total_generation_logs=int(gl_count or 0),
            total_ratings=int(vr_count or 0),
            avg_aesthetic_score=float(avg_aesthetic) if avg_aesthetic else None,
            avg_loop_smoothness=float(avg_loop) if avg_loop else None,
            avg_beat_sync=float(avg_sync) if avg_sync else None,
            labeled_count=int(labeled or 0),
            platform_breakdown=platform_breakdown,
        )
