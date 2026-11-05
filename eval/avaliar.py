"""Conceito 6 — roda eval.json e imprime recall@k, acerto, recusa e latência. (Dia 5)

Uso: docker compose run --rm dev python eval/avaliar.py
"""

import json
from pathlib import Path

CASOS = json.loads((Path(__file__).parent / "eval.json").read_text(encoding="utf-8"))


def main() -> None:
    # TODO: para cada caso, medir busca e resposta separadamente (time.perf_counter()).
    print(f"{len(CASOS)} casos carregados. Avaliação ainda não implementada.")


if __name__ == "__main__":
    main()
