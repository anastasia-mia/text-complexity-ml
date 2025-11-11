from typing import Dict, List, Tuple
from statistics import mean, pstdev
from spacy.tokens import Doc
from functools import lru_cache

try:
    from wordfreq import zipf_frequency
except Exception:
    zipf_frequency = None

try:
    from nltk.corpus import wordnet as wn
except Exception:
    wn = None

CONTENT_POS = {"NOUN", "VERB", "ADJ", "ADV", "PROPN"}
SP2WN = {"NOUN": wn.NOUN, "VERB": wn.VERB, "ADJ": wn.ADJ, "ADV": wn.ADV} if wn is not None else {}

def _alpha_tokens(doc: Doc):
    return [t for t in doc if t.is_alpha]

def _content_tokens(doc: Doc):
    return [t for t in _alpha_tokens(doc) if t.pos_ in CONTENT_POS]

@lru_cache(maxsize=100_000)
def _polysemy_cached(lemma: str, wn_pos):
    if wn is None or wn_pos is None:
        return 0
    return len(wn.synsets(lemma, pos=wn_pos))

@lru_cache(maxsize=100_000)
def _max_hyper_depth_cached(lemma: str, wn_pos):
    if wn is None or wn_pos is None:
        return 0
    depths = []
    for s in wn.synsets(lemma, pos=wn_pos):
        try:
            paths = s.hypernym_paths()
            if paths:
                depths.append(max(len(p) for p in paths))
        except Exception:
            continue
    return max(depths) if depths else 0

def sem_zipf_stats(doc: Doc) -> Dict[str, float]:
    words = _alpha_tokens(doc)
    if not words or zipf_frequency is None:
        return {
            "sem_mean_zipf": 0.0,
            "sem_share_rare_zipf_lt_4": 0.0,
            "sem_share_very_rare_zipf_lt_3": 0.0
        }
    vals = [zipf_frequency(t.lemma_.lower() or t.text.lower(), "en") for t in words]
    rare = sum(1 for v in vals if v < 4.0)
    very_rare = sum(1 for v in vals if v < 3.0)
    n = len(vals)
    return {
        "sem_mean_zipf": float(mean(vals)),
        "sem_share_rare_zipf_lt_4": rare / n,
        "sem_share_very_rare_zipf_lt_3": very_rare / n,
    }

def _lemma_synset_count(token) -> int:
    wn_pos = SP2WN.get(token.pos_)
    lemma = (token.lemma_ or token.text).lower()
    return _polysemy_cached(lemma, wn_pos)

def sem_avg_polysemy(doc: Doc) -> float:
    toks = _content_tokens(doc)
    if not toks or wn is None:
        return 0.0
    counts = [_lemma_synset_count(t) for t in toks]
    return float(mean(counts)) if counts else 0.0

def _max_hypernym_depth(token) -> int:
    wn_pos = SP2WN.get(token.pos_)
    lemma = (token.lemma_ or token.text).lower()
    return _max_hyper_depth_cached(lemma, wn_pos)

def sem_avg_hypernym_depth(doc: Doc) -> float:
    toks = _content_tokens(doc)
    if not toks or wn is None:
        return 0.0
    vals = [_max_hypernym_depth(t) for t in toks]
    return float(mean(vals)) if vals else 0.0

def _sent_vectors(doc: Doc) -> List:
    vecs = []
    for s in doc.sents:
        if hasattr(s, "vector") and s.vector is not None:
            vecs.append(s.vector)
    return vecs

def _cosine(a, b) -> float:
    import math
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)

def sem_sentence_coherence(doc: Doc) -> Dict[str, float]:
    sents = list(doc.sents)
    if len(sents) < 2:
        return {"sem_avg_sent_sim": 0.0, "sem_min_sent_sim": 0.0, "sem_std_sent_sim": 0.0}
    vecs = _sent_vectors(doc)
    if len(vecs) < 2:
        return {"sem_avg_sent_sim": 0.0, "sem_min_sent_sim": 0.0, "sem_std_sent_sim": 0.0}
    sims = []
    for i in range(len(vecs)-1):
        sims.append(_cosine(vecs[i], vecs[i+1]))
    return {
        "sem_avg_sent_sim": float(mean(sims)),
        "sem_min_sent_sim": float(min(sims)),
        "sem_std_sent_sim": float(pstdev(sims)) if len(sims) > 1 else 0.0,
    }

def sem_word_vector_dispersion(doc: Doc) -> float:
    toks = [t for t in _content_tokens(doc) if t.has_vector]
    if len(toks) < 2:
        return 0.0
    dim = len(toks[0].vector)
    centroid = [0.0] * dim
    for t in toks:
        v = t.vector
        for i in range(dim):
            centroid[i] += v[i]
    centroid = [x / len(toks) for x in centroid]

    def cos_sim(v, c):
        return _cosine(v, c)
    sims = [cos_sim(t.vector, centroid) for t in toks]

    dists = [1.0 - s for s in sims]
    return float(mean(dists))

def extract_semantics(doc: Doc) -> Dict[str, float]:
    res = {}
    res.update(sem_zipf_stats(doc))
    res["sem_avg_polysemy"] = sem_avg_polysemy(doc)
    res["sem_avg_hypernym_depth"] = sem_avg_hypernym_depth(doc)
    res.update(sem_sentence_coherence(doc))
    res["sem_word_vector_dispersion"] = sem_word_vector_dispersion(doc)
    return {k: round(float(v), 3) for k, v in res.items()}

