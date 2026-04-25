"""Tests for _sanitize() and cv_to_markdown()."""
from app import _sanitize, cv_to_markdown


class TestSanitize:
    def test_em_dash(self):
        assert _sanitize("\u2014") == "-"

    def test_en_dash(self):
        assert _sanitize("\u2013") == "-"

    def test_left_single_quote(self):
        assert _sanitize("\u2018") == "'"

    def test_right_single_quote(self):
        assert _sanitize("\u2019") == "'"

    def test_left_double_quote(self):
        assert _sanitize("\u201c") == '"'

    def test_right_double_quote(self):
        assert _sanitize("\u201d") == '"'

    def test_bullet(self):
        assert _sanitize("\u2022") == "-"

    def test_ellipsis(self):
        assert _sanitize("\u2026") == "..."

    def test_middle_dot(self):
        assert _sanitize("\u00b7") == "."

    def test_plain_ascii_unchanged(self):
        text = "Hello, World! 123"
        assert _sanitize(text) == text

    def test_mixed(self):
        assert _sanitize("foo \u2014 bar \u2019s \u2022 item") == "foo - bar 's - item"

    def test_result_encodable_to_latin1(self):
        result = _sanitize("Caf\u00e9 \u2014 na\u00efve")
        result.encode("latin-1")  # must not raise


class TestCvToMarkdown:
    def test_returns_string(self, cv):
        assert isinstance(cv_to_markdown(cv), str)

    def test_name_in_h1(self, cv):
        assert "# Ada Lovelace" in cv_to_markdown(cv)

    def test_profile_section(self, cv):
        md = cv_to_markdown(cv)
        assert "## Profile" in md
        assert "analytical engines" in md

    def test_experience_heading(self, cv):
        assert "## Professional Experience" in cv_to_markdown(cv)

    def test_highlights_company(self, cv):
        assert "### Babbage & Co" in cv_to_markdown(cv)

    def test_highlights_sub_title_bolded(self, cv):
        assert "**Analytical Engine**" in cv_to_markdown(cv)

    def test_highlights_points_as_bullets(self, cv):
        assert "- Wrote the first algorithm" in cv_to_markdown(cv)

    def test_flat_points_company(self, cv):
        assert "### Royal Society" in cv_to_markdown(cv)

    def test_flat_points_as_bullets(self, cv):
        assert "- Maintained correspondence" in cv_to_markdown(cv)

    def test_skills_section(self, cv):
        md = cv_to_markdown(cv)
        assert "## Technical Skills" in md
        assert "**Languages:**" in md

    def test_education_section(self, cv):
        md = cv_to_markdown(cv)
        assert "## Education" in md
        assert "B.Sc Mathematics" in md

    def test_contact_email(self, cv):
        assert "**Email:** ada@example.com" in cv_to_markdown(cv)

    def test_contact_github(self, cv):
        assert "**GitHub:** github.com/ada" in cv_to_markdown(cv)

    def test_contact_linkedin(self, cv):
        assert "**LinkedIn:** linkedin.com/in/ada-lovelace" in cv_to_markdown(cv)

    def test_empty_cv_does_not_crash(self):
        md = cv_to_markdown({})
        assert isinstance(md, str)
        assert "# " in md
