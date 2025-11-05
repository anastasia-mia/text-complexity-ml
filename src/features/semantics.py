from typing import Dict, List, Tuple
from statistics import mean, pstdev
from spacy.tokens import Doc
from wordfreq import zipf_frequency
from nltk.corpus import wordnet as wn

CONTENT_POS = {"NOUN", "VERB", "ADJ", "ADV", "PROPN"}

def _alpha_tokens(doc: Doc):
    return [t for t in doc if t.is_alpha]

def _content_tokens(doc: Doc):
    return [t for t in _alpha_tokens(doc) if t.pos_ in CONTENT_POS]

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
        "sem_mean_zipf": round(float(mean(vals)), 2),
        "sem_share_rare_zipf_lt_4": round(rare / n, 2),
        "sem_share_very_rare_zipf_lt_3": round(very_rare / n, 2),
    }

def _lemma_synset_count(token) -> int:
    if wn is None:
        return 0
    lemma = token.lemma_.lower() or token.text.lower()
    pos = token.pos_
    sp2wn = {"NOUN": wn.NOUN, "VERB": wn.VERB, "ADJ": wn.ADJ, "ADV": wn.ADV}
    wn_pos = sp2wn.get(pos, None)
    if wn_pos is None:
        return 0
    return len(wn.synsets(lemma, pos=wn_pos))

def sem_avg_polysemy(doc: Doc) -> float:
    toks = _content_tokens(doc)
    if not toks or wn is None:
        return 0.0
    counts = [ _lemma_synset_count(t) for t in toks ]
    return round(float(mean(counts)) if counts else 0.0, 2)

def _max_hypernym_depth(token) -> int:
    if wn is None:
        return 0
    lemma = token.lemma_.lower() or token.text.lower()
    sp2wn = {"NOUN": wn.NOUN, "VERB": wn.VERB, "ADJ": wn.ADJ, "ADV": wn.ADV}
    wn_pos = sp2wn.get(token.pos_, None)
    if wn_pos is None:
        return 0
    syns = wn.synsets(lemma, pos=wn_pos)
    if not syns:
        return 0
    depths = []
    for s in syns:
        try:
            paths = s.hypernym_paths()
            if paths:
                depths.append(max(len(p) for p in paths))
        except Exception:
            continue
    return max(depths) if depths else 0

def sem_avg_hypernym_depth(doc: Doc) -> float:
    toks = _content_tokens(doc)
    if not toks or wn is None:
        return 0.0
    vals = [_max_hypernym_depth(t) for t in toks]
    return round(float(mean(vals)) if vals else 0.0, 2)

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
        "sem_avg_sent_sim": round(float(mean(sims)), 2),
        "sem_min_sent_sim": round(float(min(sims)), 2),
        "sem_std_sent_sim": round(float(pstdev(sims)) if len(sims) > 1 else 0.0, 2),
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
    return round(float(mean(dists)), 2)

def extract_semantics(doc: Doc) -> Dict[str, float]:
    res = {}
    res.update(sem_zipf_stats(doc))
    res["sem_avg_polysemy"] = sem_avg_polysemy(doc)
    res["sem_avg_hypernym_depth"] = sem_avg_hypernym_depth(doc)
    res.update(sem_sentence_coherence(doc))
    res["sem_word_vector_dispersion"] = sem_word_vector_dispersion(doc)
    return res

