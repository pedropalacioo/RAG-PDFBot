#Concept 2 — pages -> chunks with metadata.

def chunk(pages: list[dict], size: int = 800, overlap: int = 120) -> list[dict]:
    # returns {"id": 7, "page": 3, "start": 680, "text": "chunk content..."}
    chunked_pages = []
    id = 0
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("Invalid size or overlap parameters")
    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            block = text[start:start + size]
            chunked_pages.append({"id": id, "page": page["page"], "start": start, "text": block})
            id += 1
            if start + size >= len(text):
                break
            start += size - overlap
    return chunked_pages