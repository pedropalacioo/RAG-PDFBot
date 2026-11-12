"""Concept 4 — save, load and top-k search. (Day 2)"""

from pathlib import Path

import numpy as np


def save(folder: Path, vectors: np.ndarray, chunks: list[dict]) -> None:
    # TODO: np.save for the vectors + JSON for the metadata.
    raise NotImplementedError


def load(folder: Path) -> tuple[np.ndarray, list[dict]]:
    raise NotImplementedError


def search(question_vector, vectors, chunks, k=4):
    scores = vectors @ question_vector    # no lugar de: scores = ...
    top = np.argsort(-scores)[:k]         # no lugar de: np.argsort(...)
    return [{**chunks[i], "score": float(scores[i])} for i in top]
