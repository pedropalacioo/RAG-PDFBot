# PDF -> Page list with extracted text

import argparse
from collections import Counter
import math
import re
import unicodedata

import pymupdf


def _remove_repeated_margins(texts: list[str]) -> list[str]:
    """Remove matching first/last lines on >=60% of nonempty pages (min. 3).
    Count each margin separately and leave pages with fewer than three
    nonempty lines untouched. Interior occurrences are always preserved.
    """
    pages = [text.splitlines() for text in texts]
    positions = [
        [i for i, line in enumerate(lines) if line.strip()]
        for lines in pages
    ]
    threshold = max(3, math.ceil(sum(bool(p) for p in positions) * 0.6))
    counts = {"header": Counter(), "footer": Counter()}
    candidates = []
    for lines, indexes in zip(pages, positions):
        margins = {}
        if len(indexes) >= 3:
            for side, index in (("header", indexes[0]), ("footer", indexes[-1])):
                key = " ".join(unicodedata.normalize("NFKC", lines[index]).split())
                margins[side] = (index, key)
                counts[side][key] += 1
        candidates.append(margins)
    cleaned = []
    for lines, margins in zip(pages, candidates):
        removed = {
            index for side, (index, key) in margins.items()
            if counts[side][key] >= threshold
        }
        cleaned.append("\n".join(line for i, line in enumerate(lines) if i not in removed))
    return cleaned


def _remove_page_number_lines(text: str) -> str:
    """Drop the first/last nonempty line when it is only a printed page number."""
    lines = text.splitlines()
    nonempty = [i for i, line in enumerate(lines) if line.strip()]
    removed = {
        i for i in {nonempty[0], nonempty[-1]}
        if re.fullmatch(r"\d{1,4}", lines[i].strip())
    } if nonempty else set()
    return "\n".join(line for i, line in enumerate(lines) if i not in removed)


def _clear(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\u00ad\s*", "", text)           # soft hyphen: "marca\xad\nvam" -> "marcavam"
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)   # "infor-\nmação" -> "informação"
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)    # quebra simples -> espaço
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_pages(path: str, first_page: int = 1, last_page: int | None = None) -> list[dict]:
    # [{"page": int, "text": String}]
    # first_page/last_page: 1-based, inclusive; page numbers keep the original PDF numbering.
    pages = []
    with pymupdf.open(path) as doc:
        if doc.needs_pass:
            raise ValueError(f"encrypted PDF requires a password: {path}")
        last = doc.page_count if last_page is None else last_page
        if not 1 <= first_page <= last <= doc.page_count:
            raise ValueError(
                f"invalid page range {first_page}-{last} for a PDF with {doc.page_count} pages"
            )
        for page_index in range(first_page - 1, last):
            page = doc.load_page(page_index)
            raw_text = page.get_text("text")
            if not isinstance(raw_text, str):
                raise TypeError("Expected a string from page.get_text('text')")
            pages.append({"page": page_index + 1, "text": _remove_page_number_lines(raw_text)})
    cleaned_texts = _remove_repeated_margins([page["text"] for page in pages])
    pages = [
        {"page": page["page"], "text": text}
        for page, raw_text in zip(pages, cleaned_texts)
        if (text := _clear(raw_text))
    ]
    if not pages:
        raise ValueError(f"nothing to extract in {path} (scanned PDF?)")
    return pages


if __name__ == "__main__":
    # Teste manual: python -m pdfbot.extraction data/pdfs/arquivo.pdf
    parser = argparse.ArgumentParser(description="Extrai texto das páginas de um PDF.")
    parser.add_argument("path", help="Caminho do arquivo PDF")
    parser.add_argument("--first-page", type=int, default=1, help="Primeira página (1-based)")
    parser.add_argument("--last-page", type=int, default=None, help="Última página (inclusive)")
    args = parser.parse_args()
    for p in extract_pages(args.path, args.first_page, args.last_page)[:3]:
        print(f"--- page {p['page']} ---\n{p['text'][:300]}\n")
