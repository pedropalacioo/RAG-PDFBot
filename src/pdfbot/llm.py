"""Concept 5 — LLM interface (Strategy pattern). (Day 3)"""

from abc import ABC, abstractmethod
from groq import Groq
from pdfbot import config


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system: str, prompt: str) -> str: ...


class GroqProvider(LLMProvider):
    def __init__(self, model: str = config.LLM_MODEL, temperature: float = 0.2):
        if not config.GROQ_API_KEY:
            raise RuntimeError("Groq API not defined: create .env")
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = model
        self.temperature = temperature

    def generate(self, system: str, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role":"system", "content": system},
                {"role":"user", "content": prompt},
            ],
        )
        return (response.choices[0].message.content or "").strip()
