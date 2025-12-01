from pathlib import Path
from typing import Dict, List, Optional

import joblib
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.core.textnorm import normalize_text
from src.core.spacy_nlp import load_spacy_nlp
from src.features.lexical import extract_lexical
from src.features.syntax import extract_syntax
from src.features.morph import extract_morph
from src.features.semantics import extract_semantics
from src.features.readability import extract_readability
from src.config.model_config import FEATURE_ORDER, ID2LEVEL

app = FastAPI(title="Text Complexity API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def predict_from_text(text: str) -> PredictionResponse:
    metrics = compute_all_metrics(text)
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
        level_label=level,
        probabilities=probabilities,
        metrics=metrics,
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_level(
        text: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
):
    if not text and not file:
        raise HTTPException(status_code=400, detail="Додайте текст або файл!")

    if text and text.strip():
        return predict_from_text(text)

    if file is None:
        raise HTTPException(status_code=400, detail="Документ пустий! Спробуйте ще раз")

    if file.content_type not in ("text/plain", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Підтримуються лише файли з розширенням .txt")

    raw_bytes = await file.read()

    try:
        file_text = raw_bytes.decode("utf-8", errors="ignore")
    except Exception:
        raise HTTPException(status_code=400, detail="Неможливо декодувати текст")

    if not file_text.strip():
        raise HTTPException(status_code=400, detail="Файл не містить зрозумілий текст")

    return predict_from_text(file_text)






