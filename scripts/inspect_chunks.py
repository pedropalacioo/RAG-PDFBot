#Day 1 checkpoint: inspect extracted pages and 3 random chunks of a real PDF.
#Usage: PYTHONPATH=src python scripts/inspect_chunks.py data/pdfs/<file>.pdf


import random
import sys

from pdfbot import config
from pdfbot.chunking import chunk
from pdfbot.extraction import extract_pages

path = sys.argv[1] if len(sys.argv) > 1 else "data/pdfs/apostila.pdf"

pages = extract_pages(path)
print(f"{len(pages)} pages with text")
for p in pages[:1] + pages[9:10]:
    print(f"\n=== page {p['page']} ===\n{p['text'][:1500]}")

chunks = chunk(pages, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
sizes = [len(c["text"]) for c in chunks]
print(f"\n{len(chunks)} chunks · min {min(sizes)} · avg {sum(sizes) // len(sizes)} · max {max(sizes)}")
for c in random.sample(chunks, min(3, len(chunks))):
    print(f"\n--- chunk {c['id']} (p. {c['page']}, start {c['start']}) ---\n{c['text']}")
