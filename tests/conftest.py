import os

import pytest

# Must be set before app is imported anywhere in the test session.
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-for-pytest")
os.environ.setdefault("STATIC_BUILD", "false")

import app as flask_app  # noqa: E402

MINIMAL_CV = {
    "personal": {
        "name": "Ada Lovelace",
        "title": "Test Engineer",
        "location": "London, UK",
        "phone": "+44 20 0000 0000",
        "email": "ada@example.com",
        "github": "ada",
        "linkedin": "ada-lovelace",
    },
    "profile": "A dedicated engineer with experience in analytical engines.",
    "experience": [
        {
            "company": "Babbage & Co",
            "title": "Principal Programmer",
            "period": "1842 \u2013 1843",
            "location": "London, UK",
            "highlights": [
                {
                    "title": "Analytical Engine",
                    "points": [
                        "Wrote the first algorithm intended for a machine.",
                        "Translated Menabrea\u2019s paper with extensive notes.",
                    ],
                }
            ],
        },
        {
            "company": "Royal Society",
            "title": "Correspondent",
            "period": "1840 \u2013 1842",
            "location": "London, UK",
            "points": [
                "Maintained correspondence with leading mathematicians.",
                "Presented findings on iterative computation.",
            ],
        },
    ],
    "skills": [
        {"category": "Languages", "items": "Python, Go, Bash"},
        {"category": "Tools", "items": "Git, Docker"},
    ],
    "education": [
        {
            "degree": "B.Sc Mathematics",
            "institution": "University of London",
            "year": "1840",
        }
    ],
}


@pytest.fixture
def cv():
    return MINIMAL_CV


@pytest.fixture
def client():
    flask_app.app.config["STATIC_BUILD"] = False
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as c:
        yield c
