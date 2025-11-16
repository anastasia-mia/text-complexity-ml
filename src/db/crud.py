from typing import Dict, Optional
from sqlalchemy.orm import Session
from src.db.models import Metrics, Level
from sqlalchemy import select

def get_level_by_id(db: Session, level_id: int) -> Optional[Level]:
    return db.get(Level, level_id)

def get_level_by_name(db: Session, level_name: str) -> Optional[Level]:
    name = level_name.strip().upper()
    stmt = select(Level).where(Level.name == name)
    return db.execute(stmt).scalar_one_or_none()

def resolve_level(db: Session, *, level_id: Optional[int] = None, level_name: Optional[str] = None) -> Level:
    if(level_id is None) == (level_name is None):
        raise ValueError("Provide exactly one of level ID or CEFR level name")

    lvl = get_level_by_id(db, level_id) if level_id is not None else get_level_by_name(db, level_name)
    if not lvl:
        raise ValueError("Level not found")
    return lvl

def insert_metrics(db: Session, metrics: Dict[str, float], level_id: Optional[int] = None,level_name: Optional[str] = None) -> Metrics:
    lvl = resolve_level(db, level_id = level_id, level_name=level_name)

    row = Metrics(level_id = lvl.id, **metrics)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row