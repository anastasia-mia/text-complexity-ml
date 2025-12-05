from typing import List

from pydantic import BaseModel


class LevelStats(BaseModel):
    level_id: int
    level_label: str
    count: int
    share: float


class StatsResponse(BaseModel):
    total_count: int
    avg_text_length: float
    levels: List[LevelStats]
