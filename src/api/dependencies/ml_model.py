from pathlib import Path
import joblib
from src.core.spacy_nlp import load_spacy_nlp

nlp = None
clf = None

def load_resources():
    global nlp, clf
    nlp = load_spacy_nlp("en_core_web_md")

    model_path = Path(__file__).resolve().parents[3] / "models" / "cefr_random_forest.pkl"
    bundle = joblib.load(model_path)

    clf = bundle["model"] if isinstance(bundle, dict) else bundle
