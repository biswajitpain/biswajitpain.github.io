#!/usr/bin/env python3
"""
Static site builder for the CV app.

Runs the Flask app via its test client and writes generated files to
_site/ ready for GitHub Pages deployment:

    _site/
      index.html       — rendered resume page
      resume.pdf       — server-generated PDF (fpdf2)
      resume.docx      — server-generated DOCX (python-docx)
      resume.txt       — plain-text Markdown
      static/          — CSS, favicon (mirrored from static/)

Usage:
    python build.py
"""
import os
import shutil
from pathlib import Path

# Must be set before importing app so Flask config picks them up.
os.environ.setdefault("STATIC_BUILD", "true")
os.environ.setdefault("ANTHROPIC_API_KEY", "build-placeholder")

import app as flask_app  # noqa: E402

BUILD = Path("_site")


def build():
    # ── clean ────────────────────────────────────────────────────────
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir()

    flask_app.app.config["STATIC_BUILD"] = True

    with flask_app.app.test_client() as client:

        def fetch(path, out, mode="wb"):
            r = client.get(path)
            if r.status_code != 200:
                raise RuntimeError(f"GET {path} returned {r.status_code}")
            (BUILD / out).open(mode).write(r.data)
            size = f"{len(r.data):,} bytes"
            print(f"  {out:<24} {size}")

        # Pages
        fetch("/",        "index.html",  mode="wb")   # portfolio (GitHub Pages entry point)
        fetch("/resume",  "resume.html", mode="wb")   # full CV page
        # Downloads (DOCX is local-dev only — not included in static build)
        fetch("/download/txt", "resume.txt", mode="wb")
        fetch("/download/pdf", "resume.pdf", mode="wb")

    # ── static assets ────────────────────────────────────────────────
    shutil.copytree("static", BUILD / "static")
    print(f"  static/")

    # Disable Jekyll so GitHub Pages serves the HTML as-is
    (BUILD / ".nojekyll").touch()
    print(f"  .nojekyll")

    print(f"\n  Build complete → {BUILD}/  "
          f"({sum(f.stat().st_size for f in BUILD.rglob('*') if f.is_file()):,} bytes total)")


if __name__ == "__main__":
    build()
