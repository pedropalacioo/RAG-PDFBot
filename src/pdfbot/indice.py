"""Conceito 4 — salvar, carregar e buscar top-k. (Dia 2)"""

from pathlib import Path

import numpy as np


def salvar(pasta: Path, vetores: np.ndarray, chunks: list[dict]) -> None:
    # TODO: np.save para os vetores + JSON para os metadados.
    raise NotImplementedError


def carregar(pasta: Path) -> tuple[np.ndarray, list[dict]]:
    raise NotImplementedError


def buscar(vetor_pergunta: np.ndarray, vetores: np.ndarray, chunks: list[dict], k: int = 4) -> list[dict]:
    """Retorna os k chunks mais próximos, cada um com a chave "score"."""
    # TODO: produto escalar (= cosseno com vetores normalizados) + argsort.
    raise NotImplementedError
