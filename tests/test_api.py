from fastapi.testclient import TestClient

from pdfbot.api import app

client = TestClient(app)


def test_saude():
    resposta = client.get("/saude")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}
