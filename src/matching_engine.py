import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .preprocessing import normalize_text


def calculate_text_relevance(resume_text: str, job_text: str) -> float:
    if not resume_text or not job_text:
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=5000)
    matrix = vectorizer.fit_transform([normalize_text(resume_text), normalize_text(job_text)])
    return float(round(cosine_similarity(matrix[0], matrix[1])[0][0] * 100, 2))


def calculate_skill_match(resume_skills: list[str], required_skills: list[str], preferred_skills: list[str]) -> dict:
    resume_set = {skill.lower() for skill in resume_skills}
    required_set = {skill.lower() for skill in required_skills}
    preferred_set = {skill.lower() for skill in preferred_skills}

    required_matches = sorted(skill for skill in required_skills if skill.lower() in resume_set)
    required_missing = sorted(skill for skill in required_skills if skill.lower() not in resume_set)
    preferred_matches = sorted(skill for skill in preferred_skills if skill.lower() in resume_set)
    preferred_missing = sorted(skill for skill in preferred_skills if skill.lower() not in resume_set)

    required_score = (len(required_matches) / len(required_set) * 100) if required_set else 100.0
    preferred_score = (len(preferred_matches) / len(preferred_set) * 100) if preferred_set else 100.0
    combined_score = required_score * 0.8 + preferred_score * 0.2

    return {
        "required_matches": required_matches,
        "required_missing": required_missing,
        "preferred_matches": preferred_matches,
        "preferred_missing": preferred_missing,
        "required_score": round(required_score, 2),
        "preferred_score": round(preferred_score, 2),
        "skill_match_score": round(combined_score, 2),
    }


def extract_resume_experience_years(resume_text: str) -> float:
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|yrs?)", resume_text, flags=re.IGNORECASE)
    if not matches:
        return 0.0
    return max(float(value) for value in matches)


def calculate_experience_relevance(resume_text: str, requirement: str) -> float:
    if requirement.lower() in ("", "not specified"):
        return 100.0
    required_match = re.search(r"(\d+(?:\.\d+)?)", requirement)
    if not required_match:
        return 100.0
    required_years = float(required_match.group(1))
    actual_years = extract_resume_experience_years(resume_text)
    if not actual_years:
        return 50.0
    return round(min(actual_years / required_years, 1.0) * 100, 2)
