import hashlib
import uuid
from pathlib import Path

import streamlit as st

from src.ats_analyzer import analyze_ats_keywords, build_skill_gap
from src.config import UPLOAD_DIR
from src.database import initialize_database, save_analysis
from utils.job_matcher import (
    analyze_job_description,
    calculate_experience_relevance,
    calculate_skill_match,
    calculate_text_relevance,
)
from src.recommendation_engine import (
    analyze_resume_sections,
    generate_recommendations,
    suggest_job_roles,
)
from src.report_generator import generate_pdf_report
from utils.resume_parser import ResumeUploadError, parse_resume, validate_resume
from src.scoring_engine import calculate_overall_score, completeness_score, readability_score
from src.semantic_matcher import calculate_semantic_similarity
from src.skill_extractor import extract_skills
from ui.application import render_application
from ui.theme import load_theme


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)
load_theme()
initialize_database()

SAMPLE_JD = """Senior Python Developer

We are looking for an experienced Python developer to build reliable APIs and data services.

Required:
- 3+ years of Python development experience
- SQL and PostgreSQL
- REST APIs and FastAPI or Django
- Git and Docker
- Unit testing and clear communication

Preferred:
- AWS or Azure
- Kubernetes
- pandas and scikit-learn
"""


def run_analysis(uploaded, job_text: str, job_title: str, company: str) -> dict:
    temporary_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{Path(uploaded.name).suffix.lower()}"
    try:
        validate_resume(uploaded.name, uploaded.size, uploaded.getvalue())
        temporary_path.write_bytes(uploaded.getvalue())
        resume = parse_resume(temporary_path)
        resume_skills = extract_skills(resume["text"])
        job = analyze_job_description(job_text)
        if job_title.strip():
            job["job_title"] = job_title.strip()
        job["company"] = company.strip()

        skill_match = calculate_skill_match(
            resume_skills["skills"], job["required_skills"], job["preferred_skills"]
        )
        tfidf_relevance = calculate_text_relevance(resume["text"], job_text)
        semantic_match = calculate_semantic_similarity(resume["text"], job_text)
        experience_relevance = calculate_experience_relevance(
            resume["text"], job["experience_requirement"]
        )
        completeness, missing_sections = completeness_score(resume["sections"])
        readability, formatting_issues = readability_score(resume["text"])
        ats_analysis = analyze_ats_keywords(
            resume["text"], job_text, job["required_skills"], job["preferred_skills"]
        )

        scores = {
            "skill_match": skill_match["skill_match_score"],
            "text_relevance": semantic_match["score"],
            "tfidf_relevance": tfidf_relevance,
            "experience_relevance": experience_relevance,
            "completeness": completeness,
            "readability": readability,
        }
        scores["overall"] = calculate_overall_score(scores)

        recommendations = generate_recommendations(
            skill_match, missing_sections, formatting_issues, resume_skills["skills"]
        )
        job["description_hash"] = hashlib.sha256(job_text.encode("utf-8")).hexdigest()

        result = {
            "candidate": resume["contact"],
            "sections": resume["sections"],
            "resume_skills": resume_skills,
            "job": job,
            "skill_match": skill_match,
            "scores": scores,
            "formatting_issues": formatting_issues,
            "recommendations": recommendations,
            "semantic_match": semantic_match,
            "ats_analysis": ats_analysis,
            "skill_gaps": build_skill_gap(skill_match),
            "section_suggestions": analyze_resume_sections(resume["sections"], resume["text"]),
            "role_recommendations": suggest_job_roles(resume_skills["skills"]),
        }
        report_path = generate_pdf_report(result)
        result["report_path"] = str(report_path)
        result["analysis_id"] = save_analysis(result)
        generate_pdf_report(result, report_path)
        return result
    finally:
        if temporary_path.exists():
            temporary_path.unlink(missing_ok=True)


render_application(run_analysis, SAMPLE_JD, ResumeUploadError)
