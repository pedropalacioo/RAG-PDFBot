"""FastAPI API. (Day 4)"""

from fastapi import FastAPI, HTTPException, UploadFile

app = FastAPI(title="PDF Bot with RAG")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/documents")
def upload_document(file: UploadFile) -> dict:
    # TODO: save to config.PDFS_DIR, extract, split, encode and save the index.
    raise HTTPException(status_code=501, detail="Not implemented yet")


@app.post("/questions")
def ask() -> dict:
    # TODO: Pydantic request/response schemas; call rag.answer.
    raise HTTPException(status_code=501, detail="Not implemented yet")
