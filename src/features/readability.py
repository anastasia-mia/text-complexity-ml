from typing import Dict
import textstat

def extract_readability(text: str) -> Dict[str, float]:
    if textstat is None or not text or not text.strip():
        return {
            "read_flesch": 0.0,
            "read_fkgl": 0.0,
            "read_fog": 0.0,
            "read_smog": 0.0,
            "read_dale_chall": 0.0
        }

    textstat.set_lang("en")

    res = {
        "read_flesch": textstat.flesch_reading_ease(text),
        "read_fkgl": textstat.flesch_kincaid_grade(text),
        "read_fog": textstat.gunning_fog(text),
        "read_smog": textstat.smog_index(text),
        "read_dale_chall": textstat.dale_chall_readability_score(text)
    }

    return {k: round(float(v), 2) for k, v in res.items()}