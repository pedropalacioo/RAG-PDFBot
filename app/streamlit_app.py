"""Streamlit interface: only talks to the API, never imports pdfbot directly. (Day 4)"""

import os

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.title("PDF Bot with RAG")

try:
    requests.get(f"{API_URL}/health", timeout=3).raise_for_status()
    st.success(f"API connected at {API_URL}")
except requests.RequestException:
    st.error(f"API unavailable at {API_URL}")

# TODO: PDF upload (POST /documents), question field (POST /questions)
# and the sources below the answer.
