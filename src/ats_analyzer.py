import re

from .preprocessing import tokenize, unique


STOPWORDS = {
    "and", "or", "the", "a", "an", "to", "of", "for", "in", "on", "with", "as",
    "is", "are", "be", "will", "our", "you", "your", "we", "that", "this",
}


def extract_important_keywords(job_text: str, limit: int = 40) -> list[str]:
    counts = {}
    lower = job_text.lower()
    for token in re.findall(r"(?<!\w)[a-z][a-z0-9+#.-]{2,}(?!\w)", lower):
        if token not in STOPWORDS:
            counts[token] = counts.get(token, 0) + 1
    return [word for word, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]]


def analyze_ats_keywords(resume_text: str, job_text: str, required_skills: list[str], preferred_skills: list[str]) -> dict:
    resume_lower = f" {resume_text.lower()} "
    job_keywords = extract_important_keywords(job_text)
    matched = []
    missing = []
    for keyword in job_keywords:
        if re.search(r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])", resume_lower):
            matched.append(keyword)
        else:
            missing.append(keyword)

    required_lower = {skill.lower() for skill in required_skills}
    preferred_lower = {skill.lower() for skill in preferred_skills}
    mandatory = [keyword for keyword in missing if keyword.lower() in required_lower]
    optional = [keyword for keyword in missing if keyword.lower() in preferred_lower]

    score = round(len(matched) / len(job_keywords) * 100, 2) if job_keywords else 100.0
    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "mandatory_missing": mandatory,
        "preferred_missing": optional,
        "job_keywords": job_keywords,
    }


def build_skill_gap(skill_match: dict) -> list[dict]:
    gaps = []
    for skill in skill_match["required_missing"]:
        gaps.append({
            "skill": skill,
            "importance": "Mandatory",
            "why": "The job description identifies this as a required capability.",
            "learning_topics": learning_topics_for_skill(skill),
        })
    for skill in skill_match["preferred_missing"]:
        gaps.append({
            "skill": skill,
            "importance": "Preferred",
            "why": "This skill may strengthen alignment but is not identified as mandatory.",
            "learning_topics": learning_topics_for_skill(skill),
        })
    return gaps


def learning_topics_for_skill(skill: str) -> list[str]:
    return {
        "Python": ["Python syntax", "standard library", "testing", "packaging"],
        "SQL": ["joins", "window functions", "query optimization", "indexes"],
        "Docker": ["containers", "Dockerfiles", "compose", "container security"],
        "AWS": ["core AWS services", "IAM", "deployment", "billing and monitoring"],
        "FastAPI": ["routing", "Pydantic", "dependency injection", "async APIs"],
        "Machine Learning": ["data preparation", "model evaluation", "bias", "deployment"],
        "Git": ["branching", "merging", "pull requests", "conflict resolution"],
    }.get(skill, [f"{skill} fundamentals", f"{skill} practical projects", f"{skill} documentation"])
