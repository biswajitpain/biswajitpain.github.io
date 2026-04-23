# biswajitpain.github.io

Personal CV site for **Biswajit Pain** — Systems Development Engineer, Berlin.

Built with Python / Flask. Generates a professional resume from a single YAML
config file and publishes a static version to GitHub Pages on every push.

---

## Features

| Feature | Description |
|---|---|
| **Single source of truth** | Edit `cv_config.yaml` — all outputs regenerate automatically |
| **Web** | Responsive resume page served by Flask |
| **PDF download** | Server-generated A4 PDF via `fpdf2` (no system dependencies) |
| **DOCX download** | Professional Word document via `python-docx` (local dev only) |
| **Plain text** | Markdown export |
| **AI CV generation** | Paste a job description → Claude tailors the CV in real time (local dev only) |
| **GitHub Pages** | Static HTML + PDF + plain text auto-deployed on every push to `base` |

---

## Project structure

```
cv_config.yaml        ← edit this to update your CV
app.py                ← Flask application (all routes)
build.py              ← static site generator (_site/)
requirements.txt      ← Python dependencies
Procfile              ← gunicorn entry point (production)
.env.example          ← environment variable template

templates/
  base.html           ← nav, footer, shared <head>
  index.html          ← resume page (Jinja2, renders cv_config.yaml)
  generate.html       ← AI CV generation form + live streaming preview

static/
  css/style.css       ← screen styles
  css/print.css       ← print / PDF styles
  favicon.ico

.github/workflows/
  python.yml          ← lint → build → deploy to gh-pages
```

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/biswajitpain/biswajitpain.github.io.git
cd biswajitpain.github.io

# 2. Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Set your Anthropic API key (required for AI generation)
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY=sk-ant-...

# 4. Run locally
PORT=5001 python app.py
```

Open **http://localhost:5001**

---

## Updating your CV

Edit `cv_config.yaml` — structured YAML with sections for:

```
personal      name, title, location, phone, email, github, linkedin
profile       one-paragraph summary
experience    jobs (most recent first)
  highlights  project sub-sections (title + bullet points)
  points      flat bullet list
skills        category / items pairs
education     degree entries
```

Save the file and reload the browser. All outputs (web, PDF, DOCX, plain text)
regenerate on the next request.

> **YAML tip:** bullet points that contain `: ` (colon-space) in the middle
> must be quoted: `"Designed the system: network segmentation, logging, ..."`

---

## Routes

| Route | Description |
|---|---|
| `GET /` | Resume web page |
| `GET /download/pdf` | Download PDF (server-generated) |
| `GET /download/docx` | Download DOCX — **local dev only** |
| `GET /download/txt` | Download plain text (Markdown) |
| `GET /generate` | AI CV generation form |
| `POST /generate/stream` | SSE stream from Claude (`claude-opus-4-6`) |

---

## Deployment

### GitHub Pages (automatic)

Every push to `base` triggers the CI workflow:

1. Lint (`flake8`)
2. `python build.py` → generates `_site/` (HTML + PDF + plain text + CSS)
3. Force-push `_site/` to `gh-pages` branch
4. GitHub Pages serves the static site at `https://biswajitpain.github.io`

DOCX and AI generation are not available on GitHub Pages — they require
a running Flask server.

### Production server (Heroku / Render / Fly.io)

```bash
# Heroku example
heroku create
heroku config:set ANTHROPIC_API_KEY=sk-ant-...
git push heroku base:main
```

The `Procfile` starts gunicorn with a single sync worker and 120 s timeout
(required for Claude SSE streaming).

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes (for AI features) | Anthropic API key |
| `PORT` | No (default `5001`) | Server port |
| `FLASK_DEBUG` | No (default `false`) | Enable debug / auto-reload |
| `STATIC_BUILD` | No | Set to `true` by `build.py` — hides server-only features |

---

## License

See [LICENSE](LICENSE).

`cv_config.yaml` and `resume.md` are the personal property of Biswajit Pain
and are not licensed for reuse.

The application code (`app.py`, `build.py`, templates, stylesheets) is released
under the MIT License — see [LICENSE](LICENSE) for details.
