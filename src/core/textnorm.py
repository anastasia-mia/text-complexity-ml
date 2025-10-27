import re
import unicodedata

def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    text = text.strip()

    return text
