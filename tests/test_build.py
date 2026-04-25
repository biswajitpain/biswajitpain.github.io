"""Tests for build.py static site generation."""
import os

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "build-test-placeholder")
os.environ.setdefault("STATIC_BUILD", "true")

import build as build_mod  # noqa: E402


class TestBuild:
    @pytest.fixture(autouse=True)
    def isolated_build_dir(self, tmp_path, monkeypatch):
        fake_site = tmp_path / "_site"
        monkeypatch.setattr(build_mod, "BUILD", fake_site)
        build_mod.build()
        return fake_site

    def test_index_html_created(self, isolated_build_dir):
        assert (isolated_build_dir / "index.html").exists()

    def test_resume_pdf_created(self, isolated_build_dir):
        assert (isolated_build_dir / "resume.pdf").exists()

    def test_resume_txt_created(self, isolated_build_dir):
        assert (isolated_build_dir / "resume.txt").exists()

    def test_nojekyll_created(self, isolated_build_dir):
        assert (isolated_build_dir / ".nojekyll").exists()

    def test_static_css_style(self, isolated_build_dir):
        assert (isolated_build_dir / "static" / "css" / "style.css").exists()

    def test_static_css_print(self, isolated_build_dir):
        assert (isolated_build_dir / "static" / "css" / "print.css").exists()

    def test_static_favicon(self, isolated_build_dir):
        assert (isolated_build_dir / "static" / "favicon.ico").exists()

    def test_index_html_non_empty(self, isolated_build_dir):
        assert (isolated_build_dir / "index.html").stat().st_size > 0

    def test_resume_pdf_magic_bytes(self, isolated_build_dir):
        assert (isolated_build_dir / "resume.pdf").read_bytes()[:5] == b"%PDF-"

    def test_resume_txt_contains_name(self, isolated_build_dir):
        assert b"Biswajit Pain" in (isolated_build_dir / "resume.txt").read_bytes()

    def test_docx_not_in_static_build(self, isolated_build_dir):
        assert not (isolated_build_dir / "resume.docx").exists()
