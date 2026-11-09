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


@pytest.mark.parametrize("tail_length", [1, 49, 50])
def test_tail_length_boundary(tail_length):
    text = "a" * 800 + "b" * tail_length
    result = chunk([{"page": 1, "text": text}])
    if tail_length < 50:
        assert result == [{"id": 0, "page": 1, "start": 0, "text": text}]
    else:
        assert len(result) == 2
        assert result[0]["text"] == text[:800]
        assert result[1]["text"] == text[result[1]["start"]:]


def test_short_tail_after_word_boundary_is_absorbed():
    text = "a" * 790 + " " + "b" * 20
    assert chunk([{"page": 1, "text": text}]) == [
        {"id": 0, "page": 1, "start": 0, "text": text}
    ]


def test_absorbed_tail_preserves_overlap_and_page_boundaries():
    text = "a" * 1500 + "b" * 29
    result = chunk([
        {"page": 1, "text": text},
        {"page": 2, "text": "short"},
    ])
    assert result == [
        {"id": 0, "page": 1, "start": 0, "text": text[:800]},
        {"id": 1, "page": 1, "start": 680, "text": text[680:]},
        {"id": 2, "page": 2, "start": 0, "text": "short"},
    ]

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
