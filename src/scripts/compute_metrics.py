import argparse
import json
from pathlib import Path
from src.collector import collect_all_features

def main():
    ap = argparse.ArgumentParser(description="Compute metrics for a single text or file.")
    ap.add_argument("--text", type=str, help="Text to compute metrics for.")
    ap.add_argument("---model", type=str, default="en_core_web_md", help="Spacy model to use.")
    ap.add_argument("--file", type=str, help="Output file.")
    args = ap.parse_args()

    if args.text:
        text = args.text
    elif args.file:
        p = Path(args.file)
        if not p.exists():
            ap.error(f"FIle is not found: {p}")
        text = p.read_text(encoding="utf-8", errors="ignore")
    else:
        ap.error("Either --text or --file must be specified.")

    metrics = collect_all_features(text, spacy_model = args.model)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()