from sqlalchemy import select
from sqlalchemy.orm import Session
from src.db.models import Level

CEFR_LEVELS = {
    "A1": "Beginner",
    "A2": "Elementary",
    "B1": "Intermediate",
    "B2": "Upper Intermediate",
    "C1": "Advanced",
    "C2": "Proficient"
}

def seed_levels(db: Session):
    existing_levels = {lvl.name for lvl in db.execute(select(Level)).scalars().all()}

    new_levels = []
    for name, description in CEFR_LEVELS.items():
        if name not in existing_levels:
            new_levels.append(Level(name=name, description=description))

    if not new_levels:
        print("Levels already exist")

    db.add_all(new_levels)
    db.commit()
    print(f"Seeded {len(new_levels)} levels")