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
            end = min(start +size, len(text))
            if end < len(text):
                cut = text.rfind(" ", start, end)
                if cut > start + overlap:
                    end = cut
            # Absorb short tails before applying overlap to the next chunk.
            if 0 < len(text[end:].strip()) < 50:
                end = len(text)
            block = text[start:end].strip()
            if block:
                chunked_pages.append({"id": id, "page": page["page"], "start": start, "text": block})
                id += 1
            if end >= len(text):
                break
            next_start = end - overlap
            space = text.find(" ", next_start, end)
            start = space + 1 if space != -1 else next_start
    return chunked_pages
