"""Configuration read from environment variables (.env loaded by docker compose)."""

import os
from pathlib import Path

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")

CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", 120))
TOP_K = int(os.environ.get("TOP_K", 4))
SCORE_THRESHOLD = float(os.environ.get("SCORE_THRESHOLD", 0.3))

DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))
PDFS_DIR = DATA_DIR / "pdfs"
INDEXES_DIR = DATA_DIR / "indexes"
