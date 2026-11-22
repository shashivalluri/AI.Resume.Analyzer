from src.skill_extractor import extract_skills
from src.matching_engine import calculate_skill_match, calculate_text_relevance
from src.job_analyzer import analyze_job_description


def test_python_variants_are_recognized():
    result = extract_skills("Experienced in Python programming, python3, and pandas")
    assert "Python" in result["skills"]
    assert "Pandas" in result["skills"]


def test_unrelated_word_does_not_match_go():
    result = extract_skills("We aim to improve the process")
    assert "Go" not in result["skills"]


def test_skill_matching_distinguishes_missing():
    result = calculate_skill_match(["Python", "SQL"], ["Python", "SQL", "Docker"], ["AWS"])
    assert result["required_matches"] == ["Python", "SQL"]
    assert result["required_missing"] == ["Docker"]
    assert result["preferred_missing"] == ["AWS"]


def test_text_relevance_is_bounded():
    score = calculate_text_relevance("Python developer with SQL", "Python developer required SQL")
    assert 0 <= score <= 100


def test_job_analysis_splits_preferred_skills():
    job = analyze_job_description("Python developer required SQL and Git. Preferred: AWS and Docker. 3 years experience.")
    assert "Python" in job["required_skills"]
    assert "AWS" in job["preferred_skills"]


def test_job_title_is_detected():
    job = analyze_job_description("Senior Python Developer\nRequired: Python and SQL")
    assert job["job_title"] == "Senior Python Developer"
