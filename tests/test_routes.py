"""Tests for all HTTP routes."""
import json
import os
from unittest.mock import MagicMock, patch


class TestIndex:
    def test_status_200(self, client):
        assert client.get("/").status_code == 200

    def test_content_type_html(self, client):
        assert "text/html" in client.get("/").content_type

    def test_non_empty(self, client):
        assert len(client.get("/").data) > 0

    def test_name_in_body(self, client):
        assert b"Biswajit Pain" in client.get("/").data


class TestDownloadTxt:
    def test_status_200(self, client):
        assert client.get("/download/txt").status_code == 200

    def test_content_type(self, client):
        assert "text/plain" in client.get("/download/txt").content_type

    def test_non_empty(self, client):
        assert len(client.get("/download/txt").data) > 0

    def test_attachment_header(self, client):
        cd = client.get("/download/txt").headers.get("Content-Disposition", "")
        assert "attachment" in cd and ".txt" in cd


class TestDownloadPdf:
    def test_status_200(self, client):
        assert client.get("/download/pdf").status_code == 200

    def test_content_type(self, client):
        assert client.get("/download/pdf").content_type == "application/pdf"

    def test_non_empty(self, client):
        assert len(client.get("/download/pdf").data) > 0

    def test_pdf_magic_bytes(self, client):
        assert client.get("/download/pdf").data[:5] == b"%PDF-"


class TestDownloadDocx:
    def test_status_200(self, client):
        assert client.get("/download/docx").status_code == 200

    def test_content_type(self, client):
        assert "wordprocessingml.document" in client.get("/download/docx").content_type

    def test_non_empty(self, client):
        assert len(client.get("/download/docx").data) > 0

    def test_pk_magic_bytes(self, client):
        assert client.get("/download/docx").data[:2] == b"PK"


class TestGeneratePage:
    def test_status_200(self, client):
        assert client.get("/generate").status_code == 200

    def test_content_type_html(self, client):
        assert "text/html" in client.get("/generate").content_type

    def test_non_empty(self, client):
        assert len(client.get("/generate").data) > 0


class TestGenerateStream:
    def _events(self, data: bytes) -> list:
        events = []
        for line in data.decode().splitlines():
            if line.startswith("data: ") and line.strip() != "data: [DONE]":
                events.append(json.loads(line[6:]))
        return events

    def test_missing_role_title_returns_error(self, client):
        r = client.post("/generate/stream", data={"job_description": "Build things"})
        assert r.status_code == 200
        errors = [e["error"] for e in self._events(r.data) if "error" in e]
        assert any("required" in m.lower() for m in errors)

    def test_missing_job_description_returns_error(self, client):
        r = client.post("/generate/stream", data={"role_title": "Engineer"})
        errors = [e["error"] for e in self._events(r.data) if "error" in e]
        assert any("required" in m.lower() for m in errors)

    def test_missing_api_key_returns_error(self, client):
        saved = os.environ.pop("ANTHROPIC_API_KEY", None)
        import app as flask_app
        flask_app.app.config["TESTING"] = True
        try:
            r = client.post(
                "/generate/stream",
                data={"role_title": "Engineer", "job_description": "Build things."},
            )
            errors = [e["error"] for e in self._events(r.data) if "error" in e]
            assert any("ANTHROPIC_API_KEY" in m for m in errors)
        finally:
            if saved is not None:
                os.environ["ANTHROPIC_API_KEY"] = saved

    def test_sse_ends_with_done(self, client):
        r = client.post("/generate/stream", data={})
        assert b"data: [DONE]" in r.data

    def test_sse_content_type(self, client):
        r = client.post("/generate/stream", data={})
        assert "text/event-stream" in r.content_type

    def test_happy_path_streams_tokens(self, client):
        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_ctx)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        mock_ctx.text_stream = iter(["Hello", " world"])

        mock_client = MagicMock()
        mock_client.messages.stream.return_value = mock_ctx

        with patch("app.anthropic.Anthropic", return_value=mock_client):
            r = client.post(
                "/generate/stream",
                data={"role_title": "Engineer", "job_description": "Build things."},
            )

        assert r.status_code == 200
        assert "text/event-stream" in r.content_type
        tokens = [e["token"] for e in self._events(r.data) if "token" in e]
        assert tokens == ["Hello", " world"]
        assert b"data: [DONE]" in r.data
