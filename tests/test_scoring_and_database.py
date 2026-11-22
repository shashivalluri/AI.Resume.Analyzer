from src.scoring_engine import calculate_overall_score, completeness_score, readability_score
from src.database import initialize_database, save_analysis, list_analyses, delete_all_analyses, get_analysis


def test_overall_score_is_bounded():
    scores = {"skill_match": 80, "text_relevance": 70, "experience_relevance": 60, "completeness": 50, "readability": 90}
    assert 0 <= calculate_overall_score(scores) <= 100


def test_completeness_identifies_missing_sections():
    score, missing = completeness_score({"skills": "Python"})
    assert score < 100
    assert "Professional summary" in missing


def test_readability_returns_issues_for_short_text():
    score, issues = readability_score("Python")
    assert score < 100
    assert issues


def test_database_save_list_and_delete(tmp_path):
    db = tmp_path / "test.db"
    initialize_database(db)
    result = {
        "candidate": {"name": "Test User", "email": "test@example.com"},
        "scores": {"overall": 75, "text_relevance": 70, "skill_match": 80, "experience_relevance": 60, "completeness": 80, "readability": 85},
        "job": {"description_hash": "abc", "required_skills": ["Python"], "preferred_skills": ["Docker"], "experience_requirement": "2 years", "keywords": ["python"]},
        "skill_match": {"required_matches": ["Python"], "required_missing": [], "preferred_matches": [], "preferred_missing": ["Docker"]},
        "report_path": "",
    }
    analysis_id = save_analysis(result, db)
    history = list_analyses(db)
    assert history[0]["id"] == analysis_id
    retrieved = get_analysis(analysis_id, db)
    assert not retrieved["analysis"].get("candidate_name")
    assert retrieved["job"] is not None
    assert retrieved["skills"]
    delete_all_analyses(db)
    assert list_analyses(db) == []
