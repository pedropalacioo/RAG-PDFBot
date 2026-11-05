"""Conceito 5 — interface do LLM (padrão Strategy). (Dia 3)"""

from abc import ABC, abstractmethod


class ProvedorLLM(ABC):
    @abstractmethod
    def gerar(self, system: str, prompt: str) -> str: ...


class ProvedorGemini(ProvedorLLM):
    def gerar(self, system: str, prompt: str) -> str:
        # TODO: google-genai com temperatura baixa; chave em config.GEMINI_API_KEY.
        raise NotImplementedError
