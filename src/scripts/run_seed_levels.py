from src.db.database import SessionLocal
from src.db.seed import seed_levels

db = SessionLocal()
seed_levels(db)
db.close()