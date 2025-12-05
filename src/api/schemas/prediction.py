from pydantic import BaseModel
from typing import Dict, Optional, List

class PredictionResponse(BaseModel):
    level_id: int
    level_label: str
    probabilities: Optional[Dict[str, float]] = None
    metrics: Optional[Dict[str, float]] = None
