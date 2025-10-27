import spacy
from functools import lru_cache

@lru_cache(maxsize=1)
def load_spacy_nlp(model_name: str = "en_core_web_md"):

    try:
        nlp = spacy.load(model_name, disable=["ner"])
        return nlp
    except OSError:
        print(f"The model'{model_name}' is not found. Installing...")
        from spacy.cli import download
        download(model_name)
        nlp = spacy.load(model_name, disable=["ner"])
        return nlp