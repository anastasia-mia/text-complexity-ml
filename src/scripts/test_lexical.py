from src.core.textnorm import normalize_text
from src.core.spacy_nlp import load_spacy_nlp
from src.features.lexical import extract_lexical

nlp = load_spacy_nlp("en_core_web_md")

text = """
However, this is a very simple example. 
It demonstrates how average word length, panel TTR, and stopword share behave.
"""
doc = nlp(normalize_text(text))

print(extract_lexical(doc))