from typing import Dict
from spacy.tokens import Doc

def avg_sentence_length(doc: Doc) -> float:
    sentences = list(doc.sents)
    if sentences == 0:
        return 0.0
    length = [len([t for t in s if t.is_alpha]) for s in sentences]
    return round(sum(length) / len(length), 2)

def avg_clause_per_sentence(doc: Doc) -> float:
    sentences = list(doc.sents)
    if sentences == 0:
        return 0.0
    clauses = [sum(1 for t in s if t.pos_ in ("VERB", "AUX")) for s in sentences]
    return round(sum(clauses) / len(clauses), 2)

def share_complex_sentences(doc: Doc) -> float:
    sentences = list(doc.sents)
    if sentences == 0:
        return 0.0
    complex_sentences_count = sum(1 for s in sentences if sum(1 for t in s if t.pos_ in ("VERB", "AUX")) > 1)
    return round(complex_sentences_count / len(sentences), 2)

def share_passive_sentences(doc: Doc) -> float:
    sentences = list(doc.sents)
    if sentences == 0:
        return 0.0
    passive_sentences_count = sum(1 for s in sentences if any(t.dep_ == "auxpass" for t in s))
    return round(passive_sentences_count / len(sentences), 2)

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
    return round(sum(depths) / len(depths), 2) if depths else 0.0

def share_subordinate_conjunctions(doc: Doc) -> float:
    sub_conjs = {
        "although", "because", "before", "if", "since", "though",
        "unless", "until", "when", "whenever", "whereas", "while"
    }
    tokens = [t.text.lower() for t in doc if t.is_alpha]
    sub_conjs_count = sum(1 for t in tokens if t in sub_conjs)
    return round(sub_conjs_count / len(tokens), 2) if tokens else 0.0

def avg_coord_per_sentence(doc: Doc) -> float:
    sentences = list(doc.sents)
    if not sentences:
        return 0.0
    coord_counts = [
        sum(1 for t in s if t.dep_ in {"cc", "conj"}) for s in sentences
    ]
    return round(sum(coord_counts) / len(coord_counts), 2)

def extract_syntax(doc: Doc) -> Dict[str, float]:
    return {
        "syn_avg_sentence_length": avg_sentence_length(doc),
        "syn_avg_clause_per_sentence": avg_clause_per_sentence(doc),
        "syn_share_complex_sentences": share_complex_sentences(doc),
        "syn_share_passive_sentences": share_passive_sentences(doc),
        "syn_avg_dependency_depth": avg_dependency_depth(doc),
        "syn_share_sub_conjs": share_subordinate_conjunctions(doc),
        "syn_avg_coord_per_sentence": avg_coord_per_sentence(doc),
    }