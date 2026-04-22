import os
import json
from pathlib import Path

import anthropic
import markdown2
from dotenv import load_dotenv
from flask import (
    Flask, Response, render_template,
    send_from_directory, stream_with_context, request
)

load_dotenv()

app = Flask(__name__)

RESUME_MD = Path("resume.md")

SYSTEM_PROMPT = """You are an expert CV writer and career coach with 15+ years of experience in technical recruitment.
Your task is to tailor the candidate's existing CV for a specific role and company.

Guidelines:
- Rewrite the Profile/Summary section to directly address the role's key requirements
- Reorder and emphasise experiences and bullet points most relevant to the target role
- Mirror keywords and phrases from the job description naturally throughout the CV
- Use strong action verbs; preserve and highlight all quantified achievements
- Do NOT fabricate or invent any experience, company, technology, or achievement
- Reorder the Skills section so the most relevant skills appear first
- Keep the same general length and Markdown structure as the original CV
- Output clean Markdown only — no preamble, no commentary, no code fences"""


def read_resume() -> str:
    return RESUME_MD.read_text(encoding="utf-8")


def render_md(md_content: str) -> str:
    return markdown2.markdown(
        md_content,
        extras=["fenced-code-blocks", "tables", "strike", "header-ids"]
    )


@app.route("/")
def index():
    resume_html = render_md(read_resume())
    return render_template("index.html", resume_html=resume_html)


@app.route("/download/txt")
def download_txt():
    content = read_resume()
    return Response(
        content,
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=resume.txt"}
    )


@app.route("/download/pdf")
def download_pdf():
    return send_from_directory(
        "static", "resume.pdf",
        as_attachment=True,
        download_name="Biswajit_Pain_Resume.pdf"
    )


@app.route("/generate")
def generate():
    return render_template("generate.html")


@app.route("/generate/stream", methods=["POST"])
def generate_stream():
    role_title = request.form.get("role_title", "").strip()
    company = request.form.get("company", "").strip()
    job_description = request.form.get("job_description", "").strip()

    def error_event(msg: str):
        return f"data: {json.dumps({'error': msg})}\n\ndata: [DONE]\n\n"

    if not role_title or not job_description:
        return Response(
            error_event("Role title and job description are required."),
            mimetype="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return Response(
            error_event("ANTHROPIC_API_KEY is not configured on the server."),
            mimetype="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
        )

    resume_content = read_resume()
    user_message = f"""Here is my current CV in Markdown format:

---
{resume_content}
---

Please tailor this CV for the following position:

**Role Title:** {role_title}
**Company:** {company if company else 'Not specified'}

**Job Description / Requirements:**
{job_description}

Generate the tailored CV in clean Markdown. Start directly with the name/header — no preamble."""

    def sse_stream():
        try:
            client = anthropic.Anthropic(api_key=api_key)
            with client.messages.stream(
                model="claude-opus-4-6",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}]
            ) as stream:
                for text_chunk in stream.text_stream:
                    yield f"data: {json.dumps({'token': text_chunk})}\n\n"
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
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
