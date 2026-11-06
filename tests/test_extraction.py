from pdfbot.extraction import extract_pages
import pymupdf
import pytest

@pytest.fixture
def text_pdf(make_pdf):
    return make_pdf(["primeira pagina", "segunda pagina"])

@pytest.fixture
def pdf_blank_page(make_pdf):
    return make_pdf(["a", "", "c"])

@pytest.fixture
def empty_pdf(make_pdf):
    return make_pdf(["", ""])

@pytest.fixture
def multiline_pdf(make_pdf):
    return make_pdf(["infor-\nmacao em uma\nlinha quebrada"])

@pytest.fixture
def fake_pdf(tmp_path):
    path = tmp_path / "fake.pdf"
    path.write_text("not a pdf")
    return str(path)

@pytest.fixture
def encrypted_pdf(make_pdf):
    return make_pdf(
        ["segredo"],
        encryption=pymupdf.PDF_ENCRYPT_AES_256,
        user_pw="123",
        owner_pw="456",
    )

# Tests

def test_pdf_numbered_text(text_pdf):
    assert extract_pages(text_pdf) == [
        {"page": 1, "text": "primeira pagina"},
        {"page": 2, "text": "segunda pagina"},
    ]

def test_blank_page_with_numbering(pdf_blank_page):
    assert [p["page"] for p in extract_pages(pdf_blank_page)] == [1, 3]

def test_pdf_without_text_raises(empty_pdf):
    with pytest.raises(ValueError, match="nothing to extract"):
        extract_pages(empty_pdf)

def test_line_breaks_and_hyphenation_are_cleaned(multiline_pdf):
    assert extract_pages(multiline_pdf)[0]["text"] == "informacao em uma linha quebrada"


def test_invalid_file_raises(fake_pdf):
    with pytest.raises(pymupdf.FileDataError):
        extract_pages(fake_pdf)


def test_encrypted_pdf_raises(encrypted_pdf):
    with pytest.raises(ValueError, match="encrypted"):
        extract_pages(encrypted_pdf)

