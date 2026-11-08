import pytest
from pdfbot.chunking import chunk

PAGES = [{"page": 5, "text": "short" * 600}]

def test_short_text_becomes_one_chunk():
    pages = [{"page": 1, "text": "short"}]
    result = chunk(pages, 800, 120)
    assert result == [{"id": 0, "page": 1, "start": 0, "text": "short"}]

def test_sequential_ids_across_pages():
    pages = [{"page": 1, "text": "a" * 1000}, {"page": 2, "text": "b" * 1000}]
    assert [c["id"] for c in chunk(pages, 800, 120)] == [0, 1, 2, 3]

def test_empty_input():
    assert chunk([{"page": 1, "text": ""}], 800, 120) == []

@pytest.mark.parametrize(
    "size, overlap",
    [
        (100, 100), # -> infinite loop
        (100, 150), # size < overlap -> negative pass
        (800, -1),  # -> invalid overlap value
        (0, 0),     # -> invalid input
    ],
)

def test_invalid_parameters(size, overlap):
    with pytest.raises(ValueError):
        chunk(PAGES, size, overlap)