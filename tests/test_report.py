from PyPDF2 import PdfReader

from src.report_generator import generate_pdf_report


def test_pdf_report_creation(tmp_path):
    result = {
        "candidate": {"name": "Jane Developer", "email": "jane@example.com", "phone": "1234567890"},
        "sections": {"skills": "Python", "education": "Bachelor's degree"},
        "job": {"required_skills": ["Python"], "preferred_skills": ["Docker"]},
        "skill_match": {"required_matches": ["Python"], "required_missing": [], "preferred_matches": [], "preferred_missing": ["Docker"]},
        "scores": {"overall": 82, "skill_match": 90, "text_relevance": 75, "experience_relevance": 80, "completeness": 70, "readability": 90},
        "formatting_issues": [],
        "recommendations": ["Add Docker if genuinely experienced."],
    }
    output = generate_pdf_report(result, tmp_path / "report.pdf")
    assert output.exists()
    assert output.stat().st_size > 100
    report_text = "\n".join(page.extract_text() or "" for page in PdfReader(str(output)).pages)
    assert "AI RESUME ANALYZER" in report_text
    assert "COMPATIBILITY REPORT" in report_text
    assert "Page 1" in report_text
