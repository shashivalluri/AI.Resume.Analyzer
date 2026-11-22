import re

from .config import WEIGHTS


def completeness_score(sections: dict) -> tuple[float, list[str]]:
    required = {"summary", "professional summary", "skills", "technical skills", "experience", "work experience", "education"}
    present = set(sections)
    present_normalized = present & required
    score = len(present_normalized) / 6 * 100

    missing = []
    if not (present & {"summary", "professional summary", "profile", "objective"}):
        missing.append("Professional summary")
    if not (present & {"skills", "technical skills"}):
        missing.append("Skills section")
    if not (present & {"experience", "work experience", "employment", "employment history"}):
        missing.append("Work experience")
    if "education" not in present:
        missing.append("Education")
    if "projects" not in present:
        missing.append("Projects")
    if "certifications" not in present:
        missing.append("Certifications")
    return round(min(score, 100), 2), missing


def readability_score(text: str) -> tuple[float, list[str]]:
    issues = []
    if not text:
        return 0.0, ["Resume text is empty"]

    words = re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text)
    sentences = [item for item in re.split(r"[.!?]+", text) if item.strip()]
    word_count = len(words)
    sentence_count = max(len(sentences), 1)
    average_sentence = word_count / sentence_count

    score = 100
    if word_count < 150:
        score -= 20
        issues.append("Resume is unusually short")
    if word_count > 1500:
        score -= 10
        issues.append("Resume may be excessively long")
    if average_sentence > 35:
        score -= 15
        issues.append("Sentences may be difficult to read")
    if "\x00" in text:
        score -= 30
        issues.append("Text contains invalid characters")
    if len(text.splitlines()) < 5:
        score -= 10
        issues.append("Resume appears to have little section formatting")

    bullets = len(re.findall(r"(?m)^\s*[-*•]", text))
    if bullets == 0:
        score -= 15
        issues.append("No clear bullet points detected")

    if not re.search(r"\b(led|created|developed|implemented|improved|increased|reduced|delivered)\b", text, re.I):
        score -= 10
        issues.append("Add stronger achievement-oriented action verbs")

    score = round(max(score, 0), 2)
    return score, issues


def calculate_overall_score(scores: dict) -> float:
    overall = sum(scores[name] * WEIGHTS[name] for name in WEIGHTS)
    return round(max(0.0, min(overall, 100.0)), 2)
