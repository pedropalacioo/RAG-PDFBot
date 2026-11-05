# PDF -> Page list with extracted text

import re
import sys

import pymupdf


def _clear(text: str) -> str:
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)   # "infor-\nmação" -> "informação"
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)    # quebra simples -> espaço
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_pages(path: str) -> list[dict]:
    # [{"page": }]
    pages = []
    with pymupdf.open(path) as doc:
        for page in doc:
            text = _clear(page.get_text("text"))
            if text:
                pages.append({"page": page.number + 1, "text": text})
    if not pages:
        raise ValueError(f"nothing to extract in {path} (scanned PDF?)")
    return pages


if __name__ == "__main__":
    # Teste manual: python -m pdfbot.extraction data/pdfs/arquivo.pdf
    for p in extract_pages(sys.argv[1])[:3]:
        print(f"--- page {p['page']} ---\n{p['text'][:300]}\n")
