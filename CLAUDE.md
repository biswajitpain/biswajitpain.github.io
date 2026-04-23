# Claude Instructions — biswajitpain.github.io

## Project overview

Personal CV site for **Biswajit Pain**. A Python/Flask app that reads
`cv_config.yaml` as the single source of truth and generates:
- A live web resume (Flask, Jinja2)
- A server-side PDF (`fpdf2`)
- A Word document (`python-docx`) — **local dev only**
- A plain-text Markdown export
- A static site pushed to GitHub Pages (`gh-pages` branch)

---

## Rules — always follow these

- **Never** add `Co-Authored-By: Claude` or any Claude attribution to git commits
- **Never** commit the `.venv/` directory or `_site/` directory
- **Never** commit `.env` (contains secrets)
- Do not add docstrings, type hints, or comments to code that wasn't changed
- The CV content lives in `cv_config.yaml` — do not edit `resume.md` directly
- Bullet points in `cv_config.yaml` that contain `: ` (colon-space) must be quoted

---

## Python environment

Always use the project venv:

```bash
.venv/bin/python   # interpreter
.venv/bin/pip      # package manager
```

Install dependencies:

```bash
.venv/bin/pip install -r requirements.txt
```

---

## Key commands

### Run the dev server
```bash
FLASK_DEBUG=true PORT=5001 .venv/bin/python app.py
```
Opens at **http://localhost:5001**

### Build static site
```bash
STATIC_BUILD=true ANTHROPIC_API_KEY=test .venv/bin/python build.py
```
Outputs to `_site/` — includes `index.html`, `resume.pdf`, `resume.txt`,
`static/`, `.nojekyll`.

### Deploy to GitHub Pages
```bash
cd _site
rm -rf .git
git init -b gh-pages
git add -A
git commit -m "Deploy $(date -u +'%Y-%m-%d %H:%M UTC')"
git push --force "https://github.com/biswajitpain/biswajitpain.github.io.git" gh-pages
cd ..
```

### Smoke test all routes
```bash
ANTHROPIC_API_KEY=test .venv/bin/python -c "
import app
with app.app.test_client() as c:
    for path in ['/', '/download/pdf', '/download/docx', '/download/txt']:
        r = c.get(path)
        print(path, r.status_code, len(r.data), 'bytes')
"
```

---

## Architecture

```
cv_config.yaml          ← edit here to update the CV
app.py                  ← Flask app + CvPDF + CvDOCX classes
build.py                ← generates _site/ for GitHub Pages
templates/
  base.html             ← nav (static_build flag hides DOCX + Generate links)
  index.html            ← resume rendered from cv config dict
  generate.html         ← AI CV generation (SSE streaming via Claude)
static/css/
  style.css             ← screen styles
  print.css             ← print / PDF styles
```

## Static vs live

| Feature          | GitHub Pages (`gh-pages`) | Local dev |
|------------------|--------------------------|-----------|
| Resume HTML      | ✓                        | ✓         |
| PDF download     | ✓                        | ✓         |
| Plain text       | ✓                        | ✓         |
| DOCX download    | —                        | ✓         |
| Generate with AI | —                        | ✓         |

`STATIC_BUILD=true` is set automatically by `build.py`. Templates check the
`static_build` Jinja2 variable to hide server-only features.

---

## Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Resume page |
| GET | `/download/pdf` | PDF (fpdf2, A4) |
| GET | `/download/docx` | DOCX (python-docx, Calibri/Navy style) |
| GET | `/download/txt` | Plain text Markdown |
| GET | `/generate` | AI generation form |
| POST | `/generate/stream` | SSE stream from `claude-opus-4-6` |

---

## cv_config.yaml structure

```yaml
personal:
  name, title, location, phone, email, github, linkedin

profile: >
  One-paragraph summary (YAML folded scalar)

experience:
  - company, title, period, location
    highlights:           # project sub-sections
      - title: "..."
        points: [...]
    points: [...]         # flat bullets (no sub-sections)

skills:
  - category: "..."
    items: "comma-separated string"

education:
  - degree, institution, year
```

---

## CI/CD (`.github/workflows/python.yml`)

Triggered on push to `base`:
1. Lint with `flake8` (errors only)
2. `python build.py` → `_site/`
3. Verify required files exist
4. Force-push `_site/` to `gh-pages`

PRs run lint + build but do not deploy.

---

## Environment variables

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| `ANTHROPIC_API_KEY` | For AI features | — | `sk-ant-...` |
| `PORT` | No | `5001` | Dev server port |
| `FLASK_DEBUG` | No | `false` | Auto-reload |
| `STATIC_BUILD` | No | `false` | Set by `build.py` |
