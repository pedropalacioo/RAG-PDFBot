import pymupdf
import pytest

@pytest.fixture
def make_pdf(tmp_path):
    #returns a function: make_pdf(["texto", "",...]) -> PDF path.
    def _make(texts,name="doc.pdf", **save_options):
        path = tmp_path / name
        doc = pymupdf.open()
        for text in texts:
            page = doc.new_page()
            if text:
                page.insert_text((72, 72), text)
        doc.save(path, **save_options)
        doc.close()
        return str(path)
    return _make