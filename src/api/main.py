from pathlib import Path
from typing import Dict, List, Optional

import joblib
from fastapi import FastAPI
from pydantic import BaseModel

from src.core.textnorm import normalize_text
from src.core.spacy_nlp import load_spacy_nlp
from src.features.lexical import extract_lexical
from src.features.syntax import extract_syntax
from src.features.morph import extract_morph
from src.features.semantics import extract_semantics
from src.features.readability import extract_readability
from src.config.model_config import FEATURE_ORDER, ID2LEVEL

app = FastAPI(title="Text Complexity API", version="0.1.0")

nlp = None
clf = None


class TextRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    level_id: int
    level_label: str
    probabilities: Optional[Dict[str, float]] = None
    metrics: Optional[Dict[str, float]] = None

def compute_all_metrics(text: str) -> Dict[str, float]:
    norm_text = normalize_text(text)
    doc = nlp(norm_text)

    metrics: Dict[str, float] = {}
    metrics.update(extract_lexical(doc))
    metrics.update(extract_syntax(doc))
    metrics.update(extract_morph(doc))
    metrics.update(extract_semantics(doc))
    metrics.update(extract_readability(norm_text))

    return metrics

@app.on_event("startup")
def load_resources():
    global nlp, clf

    nlp = load_spacy_nlp("en_core_web_md")
    model_path = Path(__file__).resolve().parents[2] / "models" / "cefr_random_forest.pkl"
    bundle = joblib.load(model_path)

    if hasattr(bundle, "predict"):
        clf_loaded = bundle

    elif isinstance(bundle, dict) and "model" in bundle:
        clf_loaded = bundle["model"]
    else:
        raise RuntimeError(f"Unknown model format in {model_path}")

    clf = clf_loaded



@app.post("/predict", response_model=PredictionResponse)
def predict_level(payload: TextRequest):
    metrics = compute_all_metrics(payload.text)
    x = [metrics[name] for name in FEATURE_ORDER]

    pred_id = int(clf.predict([x])[0])
    level = ID2LEVEL.get(pred_id, "unknown")

    probabilities: Optional[Dict[str, float]] = None
    if hasattr(clf, "predict_proba"):
        probs = clf.predict_proba([x])[0]

        probabilities = {}
        for class_id, p in zip(clf.classes_, probs):
            label = ID2LEVEL.get(int(class_id), str(class_id))
            probabilities[label] = float(p)

    return PredictionResponse(
        level_id=pred_id,
        level_label=ID2LEVEL.get(pred_id, "unknown"),
        probabilities=probabilities,
        metrics=metrics
    )






