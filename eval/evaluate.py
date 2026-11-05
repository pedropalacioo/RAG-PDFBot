"""Concept 6 — runs eval.json and prints recall@k, accuracy, refusal and latency. (Day 5)

Usage: docker compose run --rm dev python eval/evaluate.py
"""

import json
from pathlib import Path

CASES = json.loads((Path(__file__).parent / "eval.json").read_text(encoding="utf-8"))


def main() -> None:
    # TODO: for each case, measure search and answer separately (time.perf_counter()).
    print(f"{len(CASES)} cases loaded. Evaluation not implemented yet.")


if __name__ == "__main__":
    main()
