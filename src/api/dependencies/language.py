from fastapi import HTTPException
from langdetect import detect, LangDetectException

def ensure_english(text: str):
    cleaned = text.strip()
    if len(cleaned) < 150:
        return

    try:
        lang = detect(cleaned)
    except LangDetectException:
        raise HTTPException(400, "Не вдалося визначити мову тексту.")

    if lang != "en":
        raise HTTPException(400, "Підтримуються лише англійські тексти.")
