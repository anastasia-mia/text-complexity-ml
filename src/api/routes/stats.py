from typing import List

from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.api.schemas.stats import StatsResponse, LevelStats
from src.config.model_config import ID2LEVEL
from src.db.database import SessionLocal
from src.db.models import AnalysisLog

router = APIRouter(tags=["stats"])


@router.get("/stats", response_model=StatsResponse)
def get_stats():
    db: Session = SessionLocal()
    try:
        total = db.query(func.count(AnalysisLog.id)).scalar() or 0

        if total == 0:
            return StatsResponse(
                total_count=0,
                avg_text_length=0.0,
                levels=[],
            )

        avg_len = db.query(func.avg(AnalysisLog.text_length)).scalar() or 0.0

        rows = (
            db.query(AnalysisLog.level_id, func.count(AnalysisLog.id))
            .group_by(AnalysisLog.level_id)
            .all()
        )

        levels: List[LevelStats] = []
        for level_id, count in rows:
            label = ID2LEVEL.get(int(level_id), str(level_id))
            share = count / total
            levels.append(
                LevelStats(
                    level_id=int(level_id),
                    level_label=label,
                    count=count,
                    share=share,
                )
            )

        return StatsResponse(
            total_count=total,
            avg_text_length=float(avg_len),
            levels=levels,
        )
    finally:
        db.close()
