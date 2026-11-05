"""Concept 4 — save, load and top-k search. (Day 2)"""

from pathlib import Path

import numpy as np


def save(folder: Path, vectors: np.ndarray, chunks: list[dict]) -> None:
    # TODO: np.save for the vectors + JSON for the metadata.
    raise NotImplementedError


def load(folder: Path) -> tuple[np.ndarray, list[dict]]:
    raise NotImplementedError


def search(question_vector: np.ndarray, vectors: np.ndarray, chunks: list[dict], k: int = 4) -> list[dict]:
    """Returns the k closest chunks, each with a "score" key."""
    # TODO: dot product (= cosine with normalized vectors) + argsort.
    raise NotImplementedError
