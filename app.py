import io
import json
import os
import textwrap
from pathlib import Path

import anthropic
import yaml
from dotenv import load_dotenv
from fpdf import FPDF
from flask import (
    Flask, Response, render_template,
    stream_with_context, request
)

load_dotenv()
app = Flask(__name__)

CONFIG_FILE = Path("cv_config.yaml")

SYSTEM_PROMPT = """You are an expert CV writer and career coach with 15+ years of experience in technical recruitment.
Your task is to tailor the candidate's existing CV for a specific role and company.

Guidelines:
- Rewrite the Profile/Summary section to directly address the role's key requirements
- Reorder and emphasise experiences and bullet points most relevant to the target role
- Mirror keywords and phrases from the job description naturally throughout
- Use strong action verbs; preserve and highlight all quantified achievements
- Do NOT fabricate or invent any experience, company, technology, or achievement
- Reorder the Skills section so the most relevant skills appear first
- Keep the same general length and structure as the original CV
- Output clean Markdown only — no preamble, no commentary, no code fences"""


# ── Config loading ────────────────────────────────────────────────────

def load_cv() -> dict:
    """Load and return the CV config from cv_config.yaml."""
    return yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))


def cv_to_markdown(cv: dict) -> str:
    """Convert CV config dict to Markdown text (used for AI and txt download)."""
    p = cv.get("personal", {})
    lines = [f"# {p.get('name', '')}"]
    lines.append("")

    contact = []
    if p.get("location"):  contact.append(f"**Location:** {p['location']}")
    if p.get("phone"):     contact.append(f"**Phone:** {p['phone']}")
    if p.get("email"):     contact.append(f"**Email:** {p['email']}")
    if p.get("github"):    contact.append(f"**GitHub:** github.com/{p['github']}")
    if p.get("linkedin"):  contact.append(f"**LinkedIn:** linkedin.com/in/{p['linkedin']}")
    for c in contact:
        lines.append(f"- {c}")
    lines.append("")

    if cv.get("profile"):
        lines += ["## Profile", "", cv["profile"].strip(), ""]

    if cv.get("experience"):
        lines += ["## Professional Experience", ""]
        for job in cv["experience"]:
            lines.append(f"### {job.get('company', '')}")
            lines.append(f"- **Position:** {job.get('title', '')}")
            lines.append(f"- **Period:** {job.get('period', '')}")
            if job.get("location"):
                lines.append(f"- **Location:** {job['location']}")
            lines.append("")
            for h in job.get("highlights", []):
                if h.get("title"):
                    lines.append(f"**{h['title']}**")
                for pt in h.get("points", []):
                    lines.append(f"- {' '.join(pt.split())}")
                lines.append("")
            for pt in job.get("points", []):
                lines.append(f"- {' '.join(pt.split())}")
            if job.get("points"):
                lines.append("")

    if cv.get("skills"):
        lines += ["## Technical Skills", ""]
        for s in cv["skills"]:
            lines.append(f"- **{s['category']}:** {s['items']}")
        lines.append("")

    if cv.get("education"):
        lines += ["## Education", ""]
        for e in cv["education"]:
            suffix = f" ({e['year']})" if e.get("year") else ""
            lines.append(f"- **{e['degree']}** — {e.get('institution', '')}{suffix}")

    return "\n".join(lines)


# ── PDF generation ────────────────────────────────────────────────────

def _sanitize(text: str) -> str:
    """Replace characters outside latin-1 with safe ASCII equivalents."""
    subs = {
        '\u2014': '-',   # em dash
        '\u2013': '-',   # en dash
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2022': '-',   # bullet
        '\u2026': '...',  # ellipsis
        '\u00b7': '.',   # middle dot  (used in header join)
    }
    for char, rep in subs.items():
        text = text.replace(char, rep)
    return text.encode('latin-1', errors='replace').decode('latin-1')


class CvPDF(FPDF):
    """Professional CV PDF built from the cv_config dict."""

    MARGIN_LR = 18
    MARGIN_TOP = 16

    # Colours
    C_TEXT      = (26, 29, 35)
    C_MUTED     = (90, 98, 112)
    C_ACCENT    = (37, 99, 235)
    C_RULE      = (210, 215, 220)

    def __init__(self, cv: dict):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.cv = cv
        self.set_margins(self.MARGIN_LR, self.MARGIN_TOP, self.MARGIN_LR)
        self.set_auto_page_break(auto=True, margin=16)
        self.add_page()
        self._build()

    # ── helpers ──────────────────────────────────────────────────────

    def _w(self):
        return self.w - 2 * self.MARGIN_LR

    def _rule(self):
        r, g, b = self.C_RULE
        self.set_draw_color(r, g, b)
        self.set_line_width(0.3)
        x = self.MARGIN_LR
        self.line(x, self.get_y(), x + self._w(), self.get_y())
        self.ln(1.5)

    def _section_title(self, text: str):
        self.ln(4)
        r, g, b = self.C_MUTED
        self.set_text_color(r, g, b)
        self.set_font("Helvetica", "B", 7.5)
        self.cell(self._w(), 4, text.upper(), ln=True)
        self._rule()
        r, g, b = self.C_TEXT
        self.set_text_color(r, g, b)

    def _bullet(self, text: str, indent: float = 4):
        clean = _sanitize(" ".join(text.split()))
        self.set_font("Helvetica", "", 8.5)
        r, g, b = self.C_TEXT
        self.set_text_color(r, g, b)
        bw = self._w() - indent
        self.set_x(self.MARGIN_LR + indent - 3)
        self.cell(3, 4.5, "-", ln=False)
        self.set_x(self.MARGIN_LR + indent)
        self.multi_cell(bw, 4.5, clean)

    def _wrapped(self, text: str, size: float = 8.5, style: str = "", color=None):
        if color:
            self.set_text_color(*color)
        else:
            self.set_text_color(*self.C_TEXT)
        self.set_font("Helvetica", style, size)
        clean = _sanitize(" ".join(text.split()))
        self.multi_cell(self._w(), 4.8, clean)

    # ── sections ─────────────────────────────────────────────────────

    def _build(self):
        self._header_block()
        if self.cv.get("profile"):
            self._profile()
        if self.cv.get("experience"):
            self._experience()
        if self.cv.get("skills"):
            self._skills()
        if self.cv.get("education"):
            self._education()

    def _header_block(self):
        p = self.cv.get("personal", {})
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*self.C_TEXT)
        self.cell(self._w(), 9, _sanitize(p.get("name", "")), ln=True)
        if p.get("title"):
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*self.C_MUTED)
            self.cell(self._w(), 5, _sanitize(p["title"]), ln=True)
        self.ln(2)
        parts = []
        if p.get("location"):  parts.append(p["location"])
        if p.get("phone"):     parts.append(p["phone"])
        if p.get("email"):     parts.append(p["email"])
        if p.get("github"):    parts.append(f"github.com/{p['github']}")
        if p.get("linkedin"):  parts.append(f"linkedin.com/in/{p['linkedin']}")
        if parts:
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*self.C_MUTED)
            self.cell(self._w(), 4, _sanitize("  .  ".join(parts)), ln=True)
        self.ln(1)
        self._rule()

    def _profile(self):
        self._section_title("Profile")
        self._wrapped(self.cv["profile"].strip(), size=8.8)
        self.ln(1)

    def _experience(self):
        self._section_title("Professional Experience")
        for job in self.cv["experience"]:
            # Job title + period on same line
            y_before = self.get_y()
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*self.C_TEXT)
            period = _sanitize(job.get("period", ""))
            pw = self.get_string_width(period) + 1
            self.cell(self._w() - pw, 5, _sanitize(job.get("title", "")), ln=False)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*self.C_MUTED)
            self.cell(pw, 5, period, align="R", ln=True)

            company = job.get("company", "")
            if job.get("location"):
                company += f"  -  {job['location']}"
            self.set_font("Helvetica", "I", 8.2)
            self.set_text_color(*self.C_MUTED)
            self.cell(self._w(), 4, _sanitize(company), ln=True)
            self.ln(1)

            for h in job.get("highlights", []):
                if h.get("title"):
                    self.set_font("Helvetica", "B", 8.2)
                    self.set_text_color(*self.C_TEXT)
                    self.set_x(self.MARGIN_LR + 2)
                    self.cell(self._w() - 2, 4, _sanitize(h["title"]), ln=True)
                for pt in h.get("points", []):
                    self._bullet(pt, indent=6)
                self.ln(0.5)

            # Flat points (no sub-sections)
            for pt in job.get("points", []):
                self._bullet(pt, indent=4)

            self.ln(2)

    def _skills(self):
        self._section_title("Technical Skills")
        for s in self.cv.get("skills", []):
            cat   = s.get("category", "")
            items = str(s.get("items", ""))
            cat_w = 38
            self.set_font("Helvetica", "B", 8.2)
            self.set_text_color(*self.C_TEXT)
            x_start = self.get_x()
            y_start = self.get_y()
            self.set_x(self.MARGIN_LR)
            self.cell(cat_w, 4.5, cat + ":", ln=False)

            self.set_font("Helvetica", "", 8.2)
            self.set_text_color(*self.C_MUTED)
            self.set_x(self.MARGIN_LR + cat_w)
            self.multi_cell(self._w() - cat_w, 4.5, items)
        self.ln(1)

    def _education(self):
        self._section_title("Education")
        for e in self.cv.get("education", []):
            self.set_font("Helvetica", "B", 8.5)
            self.set_text_color(*self.C_TEXT)
            self.cell(self._w(), 4.5, _sanitize(e.get("degree", "")), ln=True)
            inst = e.get("institution", "")
            if e.get("year"):
                inst += f"  ({e['year']})"
            self.set_font("Helvetica", "", 8.2)
            self.set_text_color(*self.C_MUTED)
            self.cell(self._w(), 4, _sanitize(inst), ln=True)


# ── Routes ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    cv = load_cv()
    return render_template("index.html", cv=cv)


@app.route("/download/txt")
def download_txt():
    cv = load_cv()
    content = cv_to_markdown(cv)
    name = cv.get("personal", {}).get("name", "resume").replace(" ", "_")
    return Response(
        content,
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={name}_CV.txt"}
    )


@app.route("/download/pdf")
def download_pdf():
    cv = load_cv()
    pdf = CvPDF(cv)
    buf = io.BytesIO(pdf.output())
    name = cv.get("personal", {}).get("name", "Resume").replace(" ", "_")
    return Response(
        buf.getvalue(),
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={name}_CV.pdf"}
    )


@app.route("/generate")
def generate():
    return render_template("generate.html")


@app.route("/generate/stream", methods=["POST"])
def generate_stream():
    role_title    = request.form.get("role_title", "").strip()
    company       = request.form.get("company", "").strip()
    job_description = request.form.get("job_description", "").strip()

    def error_sse(msg: str):
        return Response(
            f"data: {json.dumps({'error': msg})}\n\ndata: [DONE]\n\n",
            mimetype="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
        )

    if not role_title or not job_description:
        return error_sse("Role title and job description are required.")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return error_sse("ANTHROPIC_API_KEY is not configured on the server.")

    cv = load_cv()
    resume_md = cv_to_markdown(cv)

    user_message = (
        f"Here is my current CV in Markdown format:\n\n---\n{resume_md}\n---\n\n"
        f"Please tailor this CV for the following position:\n\n"
        f"**Role Title:** {role_title}\n"
        f"**Company:** {company or 'Not specified'}\n\n"
        f"**Job Description / Requirements:**\n{job_description}\n\n"
        "Generate the tailored CV in clean Markdown. "
        "Start directly with the name/header — no preamble."
    )

    def sse_stream():
        try:
            client = anthropic.Anthropic(api_key=api_key)
            with client.messages.stream(
                model="claude-opus-4-6",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}]
            ) as stream:
                for chunk in stream.text_stream:
                    yield f"data: {json.dumps({'token': chunk})}\n\n"
        except anthropic.APIError as exc:
            yield f"data: {json.dumps({'error': str(exc)})}\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(sse_stream()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


if __name__ == "__main__":
    port  = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
