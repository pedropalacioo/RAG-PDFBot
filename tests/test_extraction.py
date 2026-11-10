from pdfbot.extraction import (
    extract_pages,
    _clear,
    _remove_page_number_lines,
    _remove_repeated_margins,
)
import pdfbot.extraction
import pymupdf
import pytest
import subprocess
import sys

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

def test_ligatures_are_normalized():
    assert _clear("deﬁnition") == "definition"

@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("infor-\r\nmação em\r\noutra linha", "informação em outra linha"),
        ("uma \u00a0 palavra", "uma palavra"),
        ("primeiro\r\n\r\nsegundo", "primeiro\n\nsegundo"),
    ],
)
def test_clear_normalizes_before_cleaning(text, expected):
    assert _clear(text) == expected


def test_cli_requires_pdf_path():
    result = subprocess.run(
        [sys.executable, pdfbot.extraction.__file__],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "path" in result.stderr
    assert "Traceback" not in result.stderr

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


def test_repeated_margins_are_removed_before_normalization(make_pdf):
    path = make_pdf([
        f"Manual da empresa\nConteudo da pagina {i}\nUso interno"
        for i in range(1, 4)
    ])
    assert extract_pages(path) == [
        {"page": i, "text": f"Conteudo da pagina {i}"}
        for i in range(1, 4)
    ]


def test_frequency_counts_pages_and_preserves_interior_occurrences():
    texts = [
        f"Manual\nCorpo {i}\nManual\nRodape {i}"
        for i in range(3)
    ] + ["Capa", ""]
    assert _remove_repeated_margins(texts) == [
        f"Corpo {i}\nManual\nRodape {i}" for i in range(3)
    ] + ["Capa", ""]


@pytest.mark.parametrize("texts", [
    ["Titulo\nCorpo A\nFim", "Titulo\nCorpo B\nFim"],
    [f"Titulo\nCorpo {i}\nFim {i}" for i in range(3)]
    + [f"Outro {i}\nTexto {i}\nFinal {i}" for i in range(3)],
    ["Mesmo conteudo"] * 3,
])
def test_short_documents_infrequent_margins_and_single_lines_are_preserved(texts):
    assert _remove_repeated_margins(texts) == texts


def test_margin_matching_normalizes_whitespace_and_unicode():
    texts = [
        f"{header}\nCorpo {i}\nFim {i}"
        for i, header in enumerate(["Manual ﬁnal", "Manual final", " Manual  final "])
    ]
    assert _remove_repeated_margins(texts) == [
        f"Corpo {i}\nFim {i}" for i in range(3)
    ]



# Soft hyphen (U+00AD)

@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("marca\u00ad\nvam treze", "marcavam treze"),       # hifenização no fim da linha
        ("co\u00ad municação", "comunicação"),              # quebra já convertida em espaço
        ("pala\u00advra", "palavra"),                       # hífen invisível no meio da linha
    ],
)
def test_soft_hyphens_are_removed(text, expected):
    assert _clear(text) == expected


def test_paragraph_break_is_preserved_without_soft_hyphen():
    assert _clear("fim.\n\nInício") == "fim.\n\nInício"


# Printed page numbers

@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("281\nTexto da pagina", "Texto da pagina"),        # número no topo
        ("Texto da pagina\n281\n", "Texto da pagina"),      # número no rodapé
        ("\n  42  \nTexto\n", "\nTexto"),                    # espaços e linhas vazias em volta
        ("Texto\ncom 3 linhas\nfinal", "Texto\ncom 3 linhas\nfinal"),  # números no meio ficam
        ("1984\nTexto", "Texto"),                            # 4 dígitos ainda é número de página
        ("12345\nTexto", "12345\nTexto"),                    # 5 dígitos não é
        ("Capítulo 3\nTexto", "Capítulo 3\nTexto"),          # linha com número + texto fica
        ("", ""),
    ],
)
def test_page_number_lines_are_removed(text, expected):
    assert _remove_page_number_lines(text) == expected


def test_extract_removes_printed_page_numbers(make_pdf):
    path = make_pdf(["281\nConteudo um", "282\nConteudo dois"])
    assert [p["text"] for p in extract_pages(path)] == ["Conteudo um", "Conteudo dois"]


def test_page_with_only_a_number_is_skipped(make_pdf):
    path = make_pdf(["Conteudo", "42", "Mais conteudo"])
    assert [p["page"] for p in extract_pages(path)] == [1, 3]


# Page range

def test_page_range_keeps_original_numbering(make_pdf):
    path = make_pdf(["capa", "um", "dois", "tres", "creditos"])
    assert extract_pages(path, first_page=2, last_page=4) == [
        {"page": 2, "text": "um"},
        {"page": 3, "text": "dois"},
        {"page": 4, "text": "tres"},
    ]


def test_page_range_defaults_to_last_page(make_pdf):
    path = make_pdf(["a", "b", "c"])
    assert [p["page"] for p in extract_pages(path, first_page=2)] == [2, 3]


@pytest.mark.parametrize("first, last", [(0, 2), (3, 2), (1, 4), (4, None)])
def test_invalid_page_range_raises(make_pdf, first, last):
    path = make_pdf(["a", "b", "c"])
    with pytest.raises(ValueError, match="invalid page range"):
        extract_pages(path, first_page=first, last_page=last)


def test_margins_are_counted_only_inside_the_range(make_pdf):
    # "Rodape" aparece em 3 das 5 páginas (60%), mas só em 1 das 3 páginas do intervalo
    path = make_pdf([
        "x\nCorpo 1\nRodape",
        "x\nCorpo 2\nRodape",
        "Titulo A\nCorpo 3\nRodape",
        "Titulo B\nCorpo 4\nFim B",
        "Titulo C\nCorpo 5\nFim C",
    ])
    texts = [p["text"] for p in extract_pages(path, first_page=3, last_page=5)]
    assert texts[0] == "Titulo A Corpo 3 Rodape"
