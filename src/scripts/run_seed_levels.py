from src.db.database import SessionLocal
from src.db.seed_levels import seed_levels

db = SessionLocal()
seed_levels(db)
db.close()