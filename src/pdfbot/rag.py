"""Orchestrates: question -> search -> prompt -> answer + sources. (Day 3)"""

# The prompt stays in Portuguese on purpose: it defines the language the bot answers in.
SYSTEM = """Você responde perguntas sobre um documento.
Regras:
1. Use SOMENTE as informações do CONTEXTO.
2. Se a resposta não estiver no contexto, responda exatamente:
   "Não encontrei essa informação no documento."
3. Ao final, cite as páginas usadas no formato [p. N].
4. Responda em português, de forma direta."""


def build_prompt(question: str, passages: list[dict]) -> str:
    raise NotImplementedError


def answer(question: str) -> dict:
    """Returns {"answer": str, "sources": [int, ...]}."""
    # TODO: refuse before calling the LLM if the best score < config.SCORE_THRESHOLD.
    raise NotImplementedError
