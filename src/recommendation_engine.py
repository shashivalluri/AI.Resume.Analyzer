from typing import Iterable


def generate_recommendations(skill_result: dict, missing_sections: list[str], formatting_issues: list[str], resume_skills: list[str]) -> list[str]:
    recommendations = []
    required_missing = skill_result["required_missing"]
    preferred_missing = skill_result["preferred_missing"]

    if required_missing:
        skills = ", ".join(required_missing[:8])
        recommendations.append(
            f"Only add the required skills {skills} if you genuinely possess them. Use concrete projects or experience to demonstrate them."
        )
    if preferred_missing:
        recommendations.append(
            f"Consider developing these preferred skills: {', '.join(preferred_missing[:6])}."
        )
    for section in missing_sections:
        recommendations.append(f"Add or improve the {section} section.")
    if formatting_issues:
        recommendations.extend(formatting_issues)
    if len(resume_skills) < 5:
        recommendations.append("Expand the technical skills section with verified tools and technologies.")
    recommendations.append("Use measurable achievements, such as percentage improvements, time saved, revenue, or project scale.")
    return recommendations[:12]


def analyze_resume_sections(sections: dict, text: str) -> dict[str, list[str]]:
    suggestions: dict[str, list[str]] = {}

    summary = next((sections[key] for key in ("professional summary", "summary", "profile", "objective") if key in sections), "")
    if not summary:
        suggestions["Professional Summary"] = ["Add a 3–4 sentence summary focused on role, strongest capabilities, relevant experience, and measurable value."]
    elif len(summary.split()) < 25:
        suggestions["Professional Summary"] = ["Expand the summary with role-specific expertise and one verified accomplishment; do not add invented experience."]

    skills = next((sections[key] for key in ("skills", "technical skills") if key in sections), "")
    if not skills:
        suggestions["Technical Skills"] = ["Add a dedicated technical skills section organized by category."]

    experience = next((sections[key] for key in ("experience", "work experience", "employment", "employment history") if key in sections), "")
    if not experience:
        suggestions["Work Experience"] = ["Add a work-experience section containing truthful employer, title, dates, responsibilities, and outcomes."]
    elif not any(marker in experience.lower() for marker in ("%", "reduced", "increased", "saved", "delivered", "improved")):
        suggestions["Work Experience"] = ["Add one truthful measurable outcome to each relevant role using actions and impact."]

    if not sections.get("projects", ""):
        suggestions["Projects"] = ["Add 2–3 relevant projects with the problem, technologies, your contribution, and a verifiable outcome."]
    if not sections.get("education", ""):
        suggestions["Education"] = ["Include degree or current program, institution, and graduation year if applicable."]
    if not sections.get("certifications", ""):
        suggestions["Certifications"] = ["Include only valid, verifiable certifications and display issuer and completion date."]
    if not text:
        suggestions.setdefault("Document", []).append("The resume contains no readable text.")
    return suggestions


def suggest_job_roles(resume_skills: Iterable[str]) -> list[dict]:
    skills = {skill.lower() for skill in resume_skills}
    role_catalog = {
        "Python Developer": {"python", "django", "flask", "fastapi", "sql", "git"},
        "Data Analyst": {"sql", "pandas", "numpy", "data analysis", "data visualization", "statistics"},
        "AI/ML Engineer": {"machine learning", "python", "deep learning", "pytorch", "tensorflow", "nlp"},
        "Cloud/DevOps Engineer": {"aws", "azure", "docker", "kubernetes", "linux", "ci/cd"},
        "Frontend Developer": {"javascript", "typescript", "react", "angular", "vue.js"},
        "Backend Developer": {"java", "python", "sql", "rest apis", "git", "docker"},
    }
    roles = []
    for role, required in role_catalog.items():
        matches = sorted(skills & required)
        if matches:
            coverage = len(matches) / len(required) * 100
            roles.append({
                "role": role,
                "coverage": round(coverage, 1),
                "evidence": matches,
                "reason": f"Recommended from demonstrated overlap: {', '.join(matches)}.",
            })
    return sorted(roles, key=lambda item: item["coverage"], reverse=True)[:6]
