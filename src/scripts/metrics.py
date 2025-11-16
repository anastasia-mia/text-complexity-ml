import argparse
import json
from pathlib import Path
from typing import Optional
from src.collector import collect_all_features
from src.db.database import SessionLocal
from src.db.crud import insert_metrics

def read_text(text: Optional[str], file: Optional[str]) -> str:
    if text:
        return text
    if file:
        p=Path(file)
        if not p.exists():
            raise SystemExit("File not found")
        return p.read_text(encoding="utf-8", errors="ignore")
    raise SystemExit("Either --text or --file must be specified.")


def main():
    ap = argparse.ArgumentParser(description="Compute metrics; print JSON or save to DB.")
    ap.add_argument("--text", type=str, help="Raw text to analyze.")
    ap.add_argument("--model", type=str, default="en_core_web_md", help="Spacy model to use.")
    ap.add_argument("--file", type=str, help="Path to a UTF-8 .txt file.")

    ap.add_argument("--save-db", action="store_true", help="Save metrics to DB.")
    ap.add_argument("--level", type=str, help="CEFR level name (A1..C2).")
    ap.add_argument("--level-id", type=int, help="Level ID (FK to levels.id).")

    args = ap.parse_args()

    raw = read_text(args.text, args.file)
    metrics = collect_all_features(raw, spacy_model=args.model)

    if not args.save_db:
        print(json.dumps(metrics, indent=2, ensure_ascii=False))
        return

    if (args.level is None) and (args.level_id is None):
        raise SystemExit("When using --save-db, provide either --level or --level-id.")

    if (args.level is not None) and (args.level_id is not None):
        raise SystemExit("Provide exactly one of --level or --level-id (not both).")

    db = SessionLocal()

    try:
        row = insert_metrics(
            db,
            metrics,
            level_name=args.level,
            level_id=args.level_id,
        )
        print(f"Saved metrics id={row.id} level={args.level or args.level_id}")
    finally:
        db.close()

if __name__ == "__main__":
    main()