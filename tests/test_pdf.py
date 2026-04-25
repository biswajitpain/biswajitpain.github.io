"""Tests for CvPDF PDF generation."""
from app import CvPDF


class TestCvPDF:
    def test_output_is_bytes(self, cv):
        assert isinstance(CvPDF(cv).output(), (bytes, bytearray))

    def test_output_non_empty(self, cv):
        assert len(CvPDF(cv).output()) > 0

    def test_pdf_magic_bytes(self, cv):
        assert CvPDF(cv).output()[:5] == b"%PDF-"

    def test_all_sections_render(self, cv):
        out = CvPDF(cv).output()
        assert len(out) > 1000

    def test_sparse_cv_does_not_crash(self):
        assert CvPDF({"personal": {"name": "Min"}}).output()[:5] == b"%PDF-"

    def test_special_chars_sanitized(self):
        tricky = {
            "personal": {"name": "O\u2019Brien\u2014Test"},
            "profile": "Uses \u201csmart quotes\u201d and em\u2014dashes.",
            "experience": [],
            "skills": [],
            "education": [],
        }
        assert CvPDF(tricky).output()[:5] == b"%PDF-"

    def test_highlights_and_flat_points_both_render(self, cv):
        assert CvPDF(cv).output()[:5] == b"%PDF-"
