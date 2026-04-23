# Project Skills

Reusable workflows for working on this CV site.

---

## /build-deploy

Build the static site and push it live to GitHub Pages.

```bash
# 1. Build
STATIC_BUILD=true ANTHROPIC_API_KEY=test .venv/bin/python build.py

# 2. Deploy
cd _site
rm -rf .git
git init -b gh-pages
git add -A
git commit -m "Deploy $(date -u +'%Y-%m-%d %H:%M UTC')"
git push --force "https://github.com/biswajitpain/biswajitpain.github.io.git" gh-pages
cd ..
```

---

## /run

Start the local development server with auto-reload.

```bash
FLASK_DEBUG=true PORT=5001 .venv/bin/python app.py
```

Site: http://localhost:5001  
AI generation: http://localhost:5001/generate

---

## /update-cv

Steps to update the CV:

1. Edit `cv_config.yaml`
2. Reload http://localhost:5001 to preview
3. Test all downloads:
   - http://localhost:5001/download/pdf
   - http://localhost:5001/download/docx
   - http://localhost:5001/download/txt
4. Commit: `git add cv_config.yaml && git commit -m "Update CV"`
5. Push: `git push origin base`
6. CI auto-deploys to GitHub Pages

---

## /smoke-test

Verify all routes return 200 and correct content types.

```bash
ANTHROPIC_API_KEY=test .venv/bin/python -c "
import app
checks = [
    ('/',              200, 'text/html'),
    ('/download/pdf',  200, 'application/pdf'),
    ('/download/docx', 200, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
    ('/download/txt',  200, 'text/plain'),
    ('/generate',      200, 'text/html'),
]
with app.app.test_client() as c:
    for path, expected_status, expected_mime in checks:
        r = c.get(path)
        status = 'OK' if r.status_code == expected_status else 'FAIL'
        print(f'{status}  {path:<22} {r.status_code}  {len(r.data):>7,} bytes')
"
```

---

## /install

Set up the project from scratch.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

---

## /check-yaml

Validate `cv_config.yaml` parses correctly.

```bash
.venv/bin/python -c "
import yaml
from pathlib import Path
data = yaml.safe_load(Path('cv_config.yaml').read_text())
jobs = len(data.get('experience', []))
skills = len(data.get('skills', []))
print(f'OK — {jobs} jobs, {skills} skill categories')
print(f'Name: {data[\"personal\"][\"name\"]}')
"
```
