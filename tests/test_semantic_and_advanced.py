from src.semantic_matcher import calculate_semantic_similarity
from src.ats_analyzer import analyze_ats_keywords, build_skill_gap
from src.recommendation_engine import analyze_resume_sections, suggest_job_roles


def test_semantic_similarity_is_bounded():
    result = calculate_semantic_similarity("Python SQL developer", "Python and SQL software engineer")
    assert 0 <= result["score"] <= 100
    assert result["method"] in {"sentence-transformers", "tfidf-fallback", "none"}


def test_ats_keyword_analysis():
    result = analyze_ats_keywords("Experienced Python developer", "Python developer with Docker and SQL", ["Python", "Docker", "SQL"], [])
    assert "python" in result["matched"]
    assert "docker" in result["missing"]


def test_skill_gap_prioritizes_required():
    gaps = build_skill_gap({"required_missing": ["Docker"], "preferred_missing": ["AWS"]})
    assert gaps[0]["importance"] == "Mandatory"
    assert gaps[0]["learning_topics"]


def test_section_suggestions_do_not_fabricate_content():
    result = analyze_resume_sections({"skills": "Python"}, "Python developer")
    assert "Professional Summary" in result
    assert "Work Experience" in result


def test_job_role_recommendation_is_skill_based():
    roles = suggest_job_roles(["Python", "SQL", "FastAPI", "Docker"])
    assert roles
    assert any(role["role"] == "Python Developer" for role in roles)
