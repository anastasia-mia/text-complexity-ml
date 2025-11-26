from src.core.metrics_extractor import extract_metrics_for_text
from src.predict_level import predict_from_metrics

def predict_text_level(text: str):
    metrics = extract_metrics_for_text(text)
    level_id, probabilities = predict_from_metrics(metrics)
    return {
        "level_id": level_id,
        "probabilities": probabilities,
        "metrics": metrics
    }