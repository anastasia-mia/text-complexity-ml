from src.collector import collect_all_features

def extract_metrics_for_text(text: str, model: str = "en_core_web_md") -> dict:

    if not text or not text.strip():
        raise ValueError("Text is empty")

    metrics = collect_all_features(text, spacy_model=model)

    return metrics