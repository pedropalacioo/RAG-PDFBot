"""Orquestra: pergunta -> busca -> prompt -> resposta + fontes. (Dia 3)"""

SYSTEM = """Você responde perguntas sobre um documento.
Regras:
1. Use SOMENTE as informações do CONTEXTO.
2. Se a resposta não estiver no contexto, responda exatamente:
   "Não encontrei essa informação no documento."
3. Ao final, cite as páginas usadas no formato [p. N].
4. Responda em português, de forma direta."""


def montar_prompt(pergunta: str, trechos: list[dict]) -> str:
    raise NotImplementedError


def responder(pergunta: str) -> dict:
    """Retorna {"resposta": str, "fontes": [int, ...]}."""
    # TODO: recusar antes de chamar o LLM se o melhor score < config.LIMIAR_SCORE.
    raise NotImplementedError
