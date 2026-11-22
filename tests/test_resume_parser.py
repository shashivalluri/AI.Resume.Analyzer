from pathlib import Path

import pytest

from src.resume_parser import ResumeUploadError, validate_resume, extract_docx_text, extract_contact_info


def test_validate_pdf():
    assert validate_resume("resume.pdf", 1024) == ".pdf"


def test_reject_unsupported_extension():
    with pytest.raises(ResumeUploadError):
        validate_resume("resume.txt", 1024)


def test_reject_empty_file():
    with pytest.raises(ResumeUploadError):
        validate_resume("resume.docx", 0)


def test_reject_invalid_pdf_signature():
    with pytest.raises(ResumeUploadError):
        validate_resume("resume.pdf", 100, b"not a pdf")


def test_reject_oversize_file():
    with pytest.raises(ResumeUploadError):
        validate_resume("resume.pdf", 6 * 1024 * 1024)


def test_docx_parser(tmp_path):
    from docx import Document

    path = tmp_path / "resume.docx"
    document = Document()
    document.add_heading("Jane Developer", 0)
    document.add_heading("Skills", 1)
    document.add_paragraph("Python, SQL, and Git")
    document.save(path)

    text = extract_docx_text(path)
    assert "Python" in text
    assert "Jane Developer" in text


def test_contact_extraction_finds_urls():
    contact = extract_contact_info("Jane Developer\njane@example.com\nhttps://linkedin.com/in/jane-dev\nhttps://github.com/jane-dev\nhttps://janed.dev")
    assert contact["email"] == "jane@example.com"
    assert "linkedin.com" in contact["linkedin"]
    assert "github.com" in contact["github"]
