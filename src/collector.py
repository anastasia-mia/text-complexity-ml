from typing import Dict
from src.core.textnorm import normalize_text
from src.core.spacy_nlp import load_spacy_nlp
from src.features.lexical import extract_lexical
from src.features.syntax import extract_syntax
from src.features.morph import extract_morph
from src.features.semantics import extract_semantics
from src.features.readability import extract_readability

def collect_all_features(text: str, spacy_model: str = "en_core_web_md") -> Dict[str, float]:
    norm_text = normalize_text(text)
    nlp = load_spacy_nlp(spacy_model)
    doc = nlp(norm_text)

    metrics = {}
    metrics.update(extract_lexical(doc))
    metrics.update(extract_syntax(doc))
    metrics.update(extract_morph(doc))
    metrics.update(extract_semantics(doc))
    metrics.update(extract_readability(norm_text))

    return metrics