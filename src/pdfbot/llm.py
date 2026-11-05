"""Concept 5 — LLM interface (Strategy pattern). (Day 3)"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system: str, prompt: str) -> str: ...


class GeminiProvider(LLMProvider):
    def generate(self, system: str, prompt: str) -> str:
        # TODO: google-genai with low temperature; key in config.GEMINI_API_KEY.
        raise NotImplementedError
