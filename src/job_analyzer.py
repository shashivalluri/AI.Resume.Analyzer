import re
from .preprocessing import clean_text, keyword_candidates
from .skill_extractor import extract_skills


def split_preferred_skills(text: str) -> tuple[str, str]:
    lower = text.lower()
    positions = [p for marker in ("preferred", "nice to have", "bonus", "good to have") if (p := lower.find(marker)) >= 0]
    if not positions:
        return text, ""
    position = min(positions)
    return text[:position], text[position:]


def extract_experience_requirement(text: str) -> str:
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:to\s*\d+(?:\.\d+)?)?\s*(?:years?|yrs?)", text, flags=re.IGNORECASE)
    return match.group(0).strip() if match else "Not specified"


def extract_education(text: str) -> list[str]:
    patterns = [
        r"(?:bachelor|b\.e\.?|b\.tech|b\.sc)", r"(?:master|m\.e\.?|m\.tech|m\.sc|mba)",
        r"(?:phd|ph\.d)", r"(?:degree|degree in)",
    ]
    return [pattern.strip("(?:)").replace("\\", "") for pattern in patterns if re.search(pattern, text, re.IGNORECASE)]


def extract_job_title(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "Not specified"
    first = lines[0]
    if len(first) <= 100 and not re.search(r"\b(required|responsibilities|preferred|experience)\b", first, re.I):
        return first
    return "Not specified"


def analyze_job_description(job_text: str) -> dict:
    text = clean_text(job_text)
    if len(text) < 20:
        raise ValueError("Job description must contain at least 20 characters.")
    required_text, preferred_text = split_preferred_skills(text)
    required_skills = extract_skills(required_text)["skills"]
    preferred_skills = extract_skills(preferred_text)["skills"]
    preferred_skills = [skill for skill in preferred_skills if skill not in required_skills]
    return {
        "text": text,
        "job_title": extract_job_title(job_text),
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "experience_requirement": extract_experience_requirement(text),
        "education": extract_education(text),
        "keywords": keyword_candidates(text),
    }
