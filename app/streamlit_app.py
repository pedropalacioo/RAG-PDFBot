"""Interface Streamlit: só conversa com a API, nunca importa o pdfbot direto. (Dia 4)"""

import os

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.title("PDF Bot com RAG")

try:
    requests.get(f"{API_URL}/saude", timeout=3).raise_for_status()
    st.success(f"API conectada em {API_URL}")
except requests.RequestException:
    st.error(f"API indisponível em {API_URL}")

# TODO: upload do PDF (POST /documentos), campo de pergunta (POST /perguntas)
# e as fontes abaixo da resposta.
