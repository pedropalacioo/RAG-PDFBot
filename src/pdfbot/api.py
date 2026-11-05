"""API FastAPI. (Dia 4)"""

from fastapi import FastAPI, HTTPException, UploadFile

app = FastAPI(title="PDF Bot com RAG")


@app.get("/saude")
def saude() -> dict:
    return {"status": "ok"}


@app.post("/documentos")
def enviar_documento(arquivo: UploadFile) -> dict:
    # TODO: salvar em config.PDFS_DIR, extrair, dividir, codificar e salvar o índice.
    raise HTTPException(status_code=501, detail="Ainda não implementado")


@app.post("/perguntas")
def perguntar() -> dict:
    # TODO: schemas Pydantic de requisição/resposta; chamar rag.responder.
    raise HTTPException(status_code=501, detail="Ainda não implementado")
