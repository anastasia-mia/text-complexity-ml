from typing import Dict
from spacy.tokens import Doc
from functools import lru_cache
from pathlib import Path

CONTENT_POS = {"NOUN", "VERB", "ADJ", "ADV", "PROPN"}
FUNCTION_POS = {"ADP", "AUX", "CCONJ", "DET", "PART", "PRON", "SCONJ"}

AFFIX_FILE = Path(__file__).resolve().parents[2] / "assets" / "affixes.txt"

def _alpha_tokens(doc: Doc):
    return [t for t in doc if t.is_alpha]

def _share_by_pos(doc: Doc, pos_set) -> float:
    words = _alpha_tokens(doc)
    if not words:
        return 0.0
    pos_count = sum(1 for t in words if t.pos_ in pos_set)
    return pos_count / len(words)

def _verb_heads(doc: Doc):
    return [t for t in doc if t.pos_ == "VERB"]

def _aux_children(verb):
    return [c for c in verb.children if c.dep_ in {"aux", "auxpass"}]

def morph_share_nouns(doc: Doc) -> float:
    return _share_by_pos(doc, {"NOUN"})

def morph_share_verbs(doc: Doc) -> float:
    return _share_by_pos(doc, {"VERB"})

def morph_share_adj(doc: Doc) -> float:
    return _share_by_pos(doc, {"ADJ"})

def morph_share_adv(doc: Doc) -> float:
    return _share_by_pos(doc, {"ADV"})

def morph_share_pronouns(doc: Doc) -> float:
    return _share_by_pos(doc, {"PRON"})

def morph_share_propn(doc: Doc) -> float:
    return _share_by_pos(doc, {"PROPN"})

def morph_share_aux(doc: Doc) -> float:
    return _share_by_pos(doc, {"AUX"})

def morph_share_modals(doc: Doc) -> float:
    preds = _predicates(doc)
    if not preds:
        return 0.0
    modal_pred = sum(1 for t in preds if t.tag_ == "MD")
    return modal_pred / len(preds)

def _predicates(doc: Doc):
    return [t for t in doc if t.pos_ in {"VERB","AUX"}]

def _has_aux_link(v, lemmas=None, tags=None, deps=("aux","auxpass")) -> bool:
    lemmas = set(lemmas or [])
    tags = set(tags or [])
    for n in list(v.children) + list(v.ancestors):
        if n.dep_ in deps or n.pos_ == "AUX":
            if (not lemmas or n.lemma_ in lemmas) and (not tags or n.tag_ in tags):
                return True
    return False

def morph_tense_past_share(doc: Doc) -> float:
    preds = _predicates(doc)
    if not preds:
        return 0.0
    past_count = 0
    for t in preds:
        if t.pos_ in {"VERB", "AUX"} and "Past" in t.morph.get("Tense"):
            past_count += 1
    return past_count / len(preds)

def morph_tense_present_share(doc: Doc) -> float:
    preds = _predicates(doc)
    if not preds:
        return 0.0
    pres_count = 0
    for t in preds:
        if t.pos_ in {"VERB", "AUX"} and "Pres" in t.morph.get("Tense"):
            pres_count += 1
    return pres_count / len(preds)

def morph_share_perfect(doc: Doc) -> float:
    preds = _predicates(doc)
    if not preds:
        return 0.0
    perfect_count = 0
    for v in (t for t in doc if t.pos_ == "VERB"):
        has_have = _has_aux_link(v, lemmas={"have"})
        has_be = _has_aux_link(v, lemmas={"be"})
        is_vbn = (v.tag_ == "VBN")
        is_perfect_prog = has_have and has_be and (v.tag_ == "VBG")
        if has_have and is_vbn and not is_perfect_prog:
            perfect_count += 1
    return perfect_count / len(preds)

def morph_share_progressive(doc: Doc) -> float:
    preds = _predicates(doc)
    if not preds:
        return 0.0
    cnt = 0
    for v in (t for t in doc if t.pos_ == "VERB"):
        has_be = _has_aux_link(v, lemmas={"be"})
        has_have = _has_aux_link(v, lemmas={"have"})
        if has_be and v.tag_ == "VBG" and not has_have:
            cnt += 1
    return cnt / len(preds)

def morph_share_perfect_progressive(doc: Doc) -> float:
    preds = _predicates(doc)
    if not preds:
        return 0.0
    cnt = 0
    for v in (t for t in doc if t.pos_ == "VERB"):
        has_have = _has_aux_link(v, lemmas={"have"})
        has_be = _has_aux_link(v, lemmas={"be"})
        if has_have and has_be and (v.tag_ == "VBG"):
            cnt += 1
    return cnt / len(preds)

def morph_share_future(doc: Doc) -> float:
    preds = _predicates(doc)
    if not preds:
        return 0.0
    cnt = 0
    for v in (t for t in doc if t.pos_ == "VERB"):
        modal_future = _has_aux_link(v, lemmas={"will","shall","wo"}, tags={"MD"})
        going_to = any(tok.lemma_ == "go" and tok.tag_ == "VBG" for tok in [v]) and _has_aux_link(v, lemmas={"be"})
        if modal_future or going_to:
            cnt += 1
    return cnt / len(preds)

def morph_content_function_ratio(doc: Doc) -> float:
    words = _alpha_tokens(doc)
    if not words:
        return 0.0
    content = sum(1 for t in words if t.pos_ in CONTENT_POS)
    function = sum(1 for t in words if t.pos_ in FUNCTION_POS)
    if function == 0:
        return float(content)
    return content / function

@lru_cache(maxsize=1)
def load_affixes():
    prefixes = []
    suffixes = []
    if not AFFIX_FILE.exists():
        return prefixes, suffixes
    with open(AFFIX_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.endswith("-"):
                prefixes.append(line[:-1])
            elif line.startswith("-"):
                suffixes.append(line[1:])
    return prefixes, suffixes

PREFIXES, SUFFIXES = load_affixes()

def _count_morphemes(token) -> int:
    lemma = (token.lemma_ or token.text).lower()
    morph_count = 1

    for pref in PREFIXES:
        if lemma.startswith(pref) and len(lemma) > len(pref) + 2:
            morph_count += 1
            break

    for suf in SUFFIXES:
        if lemma.endswith(suf) and len(lemma) > len(suf) + 2:
            morph_count += 1
            break

    morph = token.morph

    if morph.get("Tense") or morph.get("VerbForm") or morph.get("Aspect"):
        morph_count += 1

    if "Plur" in morph.get("Number"):
        morph_count += 1

    deg = morph.get("Degree")
    if "Cmp" in deg or "Sup" in deg:
        morph_count += 1

    return morph_count

def morph_avg_morphemes_per_word(doc: Doc) -> float:
    words = _alpha_tokens(doc)
    if not words:
        return 0.0
    counts = [_count_morphemes(t) for t in words]
    return sum(counts) / len(counts)

def extract_morph(doc: Doc) -> Dict[str, float]:
    metrics = {
        "morph_share_nouns": morph_share_nouns(doc),
        "morph_share_verbs": morph_share_verbs(doc),
        "morph_share_adj": morph_share_adj(doc),
        "morph_share_adv": morph_share_adv(doc),
        "morph_share_pronouns": morph_share_pronouns(doc),
        "morph_share_propn": morph_share_propn(doc),
        "morph_share_aux": morph_share_aux(doc),
        "morph_share_modals": morph_share_modals(doc),
        "morph_tense_past_share": morph_tense_past_share(doc),
        "morph_tense_present_share": morph_tense_present_share(doc),
        "morph_share_perfect": morph_share_perfect(doc),
        "morph_share_progressive": morph_share_progressive(doc),
        "morph_share_perfect_progressive": morph_share_perfect_progressive(doc),
        "morph_share_future": morph_share_future(doc),
        "morph_content_function_ratio": morph_content_function_ratio(doc),
        "morph_avg_morphemes_per_word": morph_avg_morphemes_per_word(doc),
    }
    return {k: round(v, 3) for k, v in metrics.items()}




