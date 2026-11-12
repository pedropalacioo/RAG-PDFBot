"""Concept 3 — texts -> normalized vectors. (Day 2)"""

import numpy as np
from sentence_transformers import SentenceTransformer

from pdfbot import config

_model = None

def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _model

def encode(texts: list[str]) -> np.ndarray:
    return _get_model().encode(texts, normalize_embeddings=True, convert_to_numpy=True)
