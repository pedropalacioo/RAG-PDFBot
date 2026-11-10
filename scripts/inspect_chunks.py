#Day 1 checkpoint: inspect extracted pages and 3 random chunks of a real PDF.
#Usage: PYTHONPATH=src python scripts/inspect_chunks.py data/pdfs/<file>.pdf [--first-page N] [--last-page M]


import argparse
import random

from pdfbot import config
from pdfbot.chunking import chunk
from pdfbot.extraction import extract_pages

parser = argparse.ArgumentParser(description="Inspect extracted pages and random chunks.")
parser.add_argument("path", nargs="?", default="data/pdfs/apostila.pdf")
parser.add_argument("--first-page", type=int, default=1)
parser.add_argument("--last-page", type=int, default=None)
args = parser.parse_args()

pages = extract_pages(args.path, args.first_page, args.last_page)
print(f"{len(pages)} pages with text")
for p in pages[:1] + pages[9:10]:
    print(f"\n=== page {p['page']} ===\n{p['text'][:1500]}")

chunks = chunk(pages, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
sizes = [len(c["text"]) for c in chunks]
print(f"\n{len(chunks)} chunks · min {min(sizes)} · avg {sum(sizes) // len(sizes)} · max {max(sizes)}")
for c in random.sample(chunks, min(3, len(chunks))):
    print(f"\n--- chunk {c['id']} (p. {c['page']}, start {c['start']}) ---\n{c['text']}")
