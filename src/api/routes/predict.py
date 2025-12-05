from typing import Dict, Optional
from fastapi import APIRouter, Form, File, UploadFile, HTTPException
import src.api.dependencies.ml_model as ml_model
from src.api.dependencies.language import ensure_english
from src.core.textnorm import normalize_text
from src.features.lexical import extract_lexical
from src.features.syntax import extract_syntax
from src.features.morph import extract_morph
from src.features.semantics import extract_semantics
from src.features.readability import extract_readability
from src.config.model_config import FEATURE_ORDER, ID2LEVEL
from src.api.schemas.prediction import PredictionResponse
from src.db.database import SessionLocal
from src.db.models import AnalysisLog

router = APIRouter(tags=["predict"])

def compute_all_metrics(text: str) -> Dict[str, float]:
    if ml_model.nlp is None:
        raise HTTPException(
            status_code=500,
            detail="NLP-пайплайн не завантажений. Перезапустіть сервер або перевірте startup_event."
        )

    norm_text = normalize_text(text)
    doc = ml_model.nlp(norm_text)

    metrics: Dict[str, float] = {}
    metrics.update(extract_lexical(doc))
    metrics.update(extract_syntax(doc))
    metrics.update(extract_morph(doc))
    metrics.update(extract_semantics(doc))
    metrics.update(extract_readability(norm_text))

    return metrics

def predict_from_text(text: str) -> PredictionResponse:
    if ml_model.clf is None:
        raise HTTPException(
            status_code=500,
            detail="Модель класифікації не завантажена. Перезапустіть сервер."
        )

    metrics = compute_all_metrics(text)
    x = [metrics[name] for name in FEATURE_ORDER]

    pred_id = int(ml_model.clf.predict([x])[0])
    level = ID2LEVEL.get(pred_id, "unknown")

    probabilities: Optional[Dict[str, float]] = None
    if hasattr(ml_model.clf, "predict_proba"):
        probs = ml_model.clf.predict_proba([x])[0]

        probabilities = {}
        for class_id, p in zip(ml_model.clf.classes_, probs):
            label = ID2LEVEL.get(int(class_id), str(class_id))
            probabilities[label] = float(p)

    return PredictionResponse(
        level_id=pred_id,
        level_label=level,
        probabilities=probabilities,
        metrics=metrics,
    )

@router.post("/predict", response_model=PredictionResponse)
async def predict_level(text: str = Form(None), file: UploadFile = File(None)):
    MIN_CHARS: int = 150
    MAX_CHARS: int = 8000

    db = SessionLocal()

    if not text and not file:
        raise HTTPException(status_code=400, detail="Додайте текст або файл!")

    if text and text.strip():
        ensure_english(text)
        response = predict_from_text(text)

        log = AnalysisLog(
            level_id=response.level_id,
            level_label=response.level_label,
            text_length=len(text),
            source_type="text",
        )
        db.add(log)
        db.commit()
        return response


    if file is None:
        raise HTTPException(status_code=400, detail="Документ пустий! Спробуйте ще раз")

    if file.content_type not in ("text/plain", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Підтримуються лише файли з розширенням .txt")

    raw_bytes = await file.read()

    try:
        file_text = raw_bytes.decode("utf-8", errors="ignore")

        if len(file_text) < MIN_CHARS:
            raise HTTPException(400, detail=f"File text is too short ({MIN_CHARS} symbols required)")

        if len(file_text) > MAX_CHARS:
            raise HTTPException(400, detail=f"File text is too long (max {MAX_CHARS} symbols)")
    except Exception:
        raise HTTPException(status_code=400, detail="Неможливо декодувати текст")

    if not file_text.strip():
        raise HTTPException(status_code=400, detail="Файл не містить зрозумілий текст")

    ensure_english(file_text)

    response = predict_from_text(file_text)

    log = AnalysisLog(
        level_id=response.level_id,
        level_label=response.level_label,
        text_length=len(file_text),
        source_type="file",
    )
    db.add(log)
    db.commit()
    return response