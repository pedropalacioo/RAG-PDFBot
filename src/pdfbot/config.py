"""Configuração lida de variáveis de ambiente (.env carregado pelo docker compose)."""

import os
from pathlib import Path

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")

CHUNK_TAMANHO = int(os.environ.get("CHUNK_TAMANHO", 800))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", 120))
TOP_K = int(os.environ.get("TOP_K", 4))
LIMIAR_SCORE = float(os.environ.get("LIMIAR_SCORE", 0.3))

DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))
PDFS_DIR = DATA_DIR / "pdfs"
INDICES_DIR = DATA_DIR / "indices"
