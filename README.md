# PDF Bot com RAG

Responde perguntas usando apenas o conteúdo de um PDF e cita as páginas de origem.
Pipeline: extração (PyMuPDF) → chunking → embeddings (sentence-transformers) → busca top-k → LLM (Gemini) → resposta + fontes.
