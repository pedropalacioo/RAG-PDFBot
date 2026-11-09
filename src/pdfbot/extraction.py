# PDF -> Page list with extracted text

import argparse
import re
import unicodedata

import pymupdf


def _clear(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)   # "infor-\nmação" -> "informação"
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)    # quebra simples -> espaço
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_pages(path: str) -> list[dict]:
    # [{"page": int, "text": String}]
    pages = []
    with pymupdf.open(path) as doc:
        if doc.needs_pass:
            raise ValueError(f"encrypted PDF requires a password: {path}")
        for page_index in range(doc.page_count):
            page = doc.load_page(page_index)
            raw_text = page.get_text("text")
            if not isinstance(raw_text, str):
                raise TypeError("Expected a string from page.get_text('text')")
            text = _clear(raw_text)
            if text:
                pages.append({"page": page_index + 1, "text": text})
    if not pages:
        raise ValueError(f"nothing to extract in {path} (scanned PDF?)")
    return pages


if __name__ == "__main__":
    # Teste manual: python -m pdfbot.extraction data/pdfs/arquivo.pdf
    parser = argparse.ArgumentParser(description="Extrai texto das páginas de um PDF.")
    parser.add_argument("path", help="Caminho do arquivo PDF")
    args = parser.parse_args()
    for p in extract_pages(args.path)[:3]:
        print(f"--- page {p['page']} ---\n{p['text'][:300]}\n")
