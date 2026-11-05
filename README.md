# PDF Bot with RAG

Answers questions using only the content of a PDF and cites the source pages.
Pipeline: extraction (PyMuPDF) → chunking → embeddings (sentence-transformers) → top-k search → LLM (Gemini) → answer + sources.
