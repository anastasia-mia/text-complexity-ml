from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    name = Column(String(4), unique=True, nullable=False)
    description = Column(String(256), nullable=False)

    metrics = relationship("Metrics", back_populates="level")

class Metrics(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)

    lex_avg_word_len = Column(Float)
    lex_ttr_lemma = Column(Float)
    lex_share_stop = Column(Float)
    lex_share_num_symbol = Column(Float)
    lex_share_oov = Column(Float)
    lex_share_awl = Column(Float)
    lex_avg_syll_per_word = Column(Float)
    syn_avg_sentence_length = Column(Float)
    syn_avg_clause_per_sentence = Column(Float)
    syn_share_complex_sentences = Column(Float)
    syn_share_passive_sentences = Column(Float)
    syn_avg_dependency_depth = Column(Float)
    syn_share_sub_conjs = Column(Float)
    syn_avg_coord_per_sentence = Column(Float)
    morph_share_nouns = Column(Float)
    morph_share_verbs = Column(Float)
    morph_share_adj = Column(Float)
    morph_share_adv = Column(Float)
    morph_share_pronouns = Column(Float)
    morph_share_propn = Column(Float)
    morph_share_aux = Column(Float)
    morph_share_modals = Column(Float)
    morph_tense_past_share = Column(Float)
    morph_tense_present_share = Column(Float)
    morph_share_perfect = Column(Float)
    morph_share_progressive = Column(Float)
    morph_share_perfect_progressive = Column(Float)
    morph_share_future = Column(Float)
    morph_content_function_ratio = Column(Float)
    morph_avg_morphemes_per_word = Column(Float)
    sem_mean_zipf = Column(Float)
    sem_share_rare_zipf_lt_4 = Column(Float)
    sem_share_very_rare_zipf_lt_3 = Column(Float)
    sem_avg_polysemy = Column(Float)
    sem_avg_hypernym_depth = Column(Float)
    sem_avg_sent_sim = Column(Float)
    sem_min_sent_sim = Column(Float)
    sem_std_sent_sim = Column(Float)
    sem_word_vector_dispersion = Column(Float)
    read_flesch = Column(Float)
    read_fkgl = Column(Float)
    read_fog = Column(Float)
    read_smog = Column(Float)
    read_dale_chall = Column(Float)

    level = relationship("Level", back_populates="metrics")