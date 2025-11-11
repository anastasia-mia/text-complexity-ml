from typing import Dict
from spacy.tokens import Doc

def avg_sentence_length(doc: Doc) -> float:
    sentences = list(doc.sents)
    if not sentences:
        return 0.0
    length = [len([t for t in s if t.is_alpha]) for s in sentences]
    return sum(length) / len(length)

def avg_clause_per_sentence(doc: Doc) -> float:
    sentences = list(doc.sents)
    if not sentences:
        return 0.0
    clauses = [sum(1 for t in s if t.pos_ in ("VERB","AUX") and "Fin" in t.morph.get("VerbForm", [])) for s in sentences]
    return sum(clauses) / len(clauses)

def share_complex_sentences(doc: Doc) -> float:
    sentences = list(doc.sents)
    if not sentences:
        return 0.0
    complex_sentences_count = sum(1 for s in sentences if sum(1 for t in s if t.pos_ in ("VERB", "AUX")) > 1)
    return complex_sentences_count / len(sentences)

def share_passive_sentences(doc: Doc) -> float:
    sentences = list(doc.sents)
    if not sentences:
        return 0.0
    def is_passive(s):
        has_nsubjpass = any(t.dep_ == "nsubjpass" for t in s)
        be_aux = any(t.lemma_ == "be" and t.pos_ == "AUX" for t in s)
        vbn_head = any(t.tag_ == "VBN" and t.pos_ == "VERB" for t in s)
        return has_nsubjpass or (be_aux and vbn_head)
    passive_sentences_count = sum(1 for s in sentences if is_passive(s))
    return passive_sentences_count / len(sentences)

def avg_dependency_depth(doc: Doc) -> float:
    sentences = list(doc.sents)
    if not sentences:
        return 0.0

    def depth(token):
        if not list(token.children):
            return 1
        return 1 + max(depth(child) for child in token.children)

    depths = []
    for s in sentences:
        roots = [t for t in s if t.head == t]
        if roots:
            depths.append(max(depth(r) for r in roots))
    return sum(depths) / len(depths) if depths else 0.0

def share_subordinate_conjunctions(doc: Doc) -> float:
    SUB_CONJS = {
        "although", "because", "before", "if", "since", "though",
        "unless", "until", "when", "whenever", "whereas", "while"
    }
    tokens = [t for t in doc if t.is_alpha]
    sub_conjs_count = sum(1 for t in tokens if t.pos_ == "SCONJ" or t.lemma_.lower() in SUB_CONJS)
    return sub_conjs_count / len(tokens) if tokens else 0.0

def avg_coord_per_sentence(doc: Doc) -> float:
    sentences = list(doc.sents)
    if not sentences:
        return 0.0
    coord_counts = [
        sum(1 for t in s if t.dep_ in {"cc", "conj"}) for s in sentences
    ]
    return sum(coord_counts) / len(coord_counts)

def extract_syntax(doc: Doc) -> Dict[str, float]:
    metrics = {
        "syn_avg_sentence_length": avg_sentence_length(doc),
        "syn_avg_clause_per_sentence": avg_clause_per_sentence(doc),
        "syn_share_complex_sentences": share_complex_sentences(doc),
        "syn_share_passive_sentences": share_passive_sentences(doc),
        "syn_avg_dependency_depth": avg_dependency_depth(doc),
        "syn_share_sub_conjs": share_subordinate_conjunctions(doc),
        "syn_avg_coord_per_sentence": avg_coord_per_sentence(doc),
    }
    return {k: round(v, 3) for k, v in metrics.items()}