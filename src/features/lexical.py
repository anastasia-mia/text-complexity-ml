from typing import Dict, Set, Optional
from functools import lru_cache
import textstat
from pathlib import Path

def _alpha_tokens(doc):
    return [t for t in doc if t.is_alpha]

@lru_cache(maxsize=1)
def _awl_path(default: Optional[str] = None) -> Path:
    project_root = Path(__file__).resolve().parents[2]
    path = project_root / "assets" / "awl.txt"
    if default:
        return Path(default)
    return path

@lru_cache(maxsize=1)
def _load_awl(path: Optional[str] = None) -> Set[str]:
    awl_file = Path(path) if path else _awl_path()
    if not awl_file.exists():
        return set()
    with awl_file.open("r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}

def avg_word_len(doc) -> float:
    words = _alpha_tokens(doc)
    if not words:
        return 0.0
    return sum(len(t.text) for t in words) / len(words)

def type_token_ratio_lemma(doc) -> float:
    lemmas = [t.lemma_.lower() for t in _alpha_tokens(doc)]
    if not lemmas:
        return 0.0
    return len(set(lemmas)) / len(lemmas)

def share_stopwords(doc) -> float:
    words = _alpha_tokens(doc)
    if not words:
        return 0.0
    stop_count = sum(1 for t in words if t.is_stop)
    return stop_count / len(words)

def share_num_symbol(doc) -> float:
    tokens = [t for t in doc]
    if not tokens:
        return 0.0
    num_or_symbol = sum(1 for t in tokens if (t.pos_ == "NUM") or (not t.is_alpha and not t.is_space))
    return num_or_symbol / len(tokens)

def share_oov(doc) -> float:
    words = _alpha_tokens(doc)
    if not words:
        return 0.0
    oov_count = sum(1 for t in words if t.is_oov)
    return oov_count / len(words)

def share_awl(doc, awl_path: Optional[str] = None) -> float:
    words = _alpha_tokens(doc)
    if not words:
        return 0.0
    awl = _load_awl(awl_path)
    if not awl:
        return 0.0
    hits = sum(1 for t in words if t.lemma_.lower() in awl)
    return hits / len(words)

def avg_syllables_per_word(doc) -> float:
    if textstat is None:
        return 0.0
    words = _alpha_tokens(doc)
    if not words:
        return 0.0
    total_syllables = 0
    counted = 0
    for t in words:
        s = textstat.syllable_count(t.text, lang="en_US")
        if s is not None:
            total_syllables += int(s)
            counted += 1
    return (total_syllables / counted) if counted else 0.0

def extract_lexical(doc) -> Dict[str, float]:
    metrics = {
        "lex_avg_word_len": avg_word_len(doc),
        "lex_ttr_lemma": type_token_ratio_lemma(doc),
        "lex_share_stop": share_stopwords(doc),
        "lex_share_num_symbol": share_num_symbol(doc),
        "lex_share_oov": share_oov(doc),
        "lex_share_awl": share_awl(doc),
        "lex_avg_syll_per_word": avg_syllables_per_word(doc),
    }
    return {k: round(v, 2) for k, v in metrics.items()}