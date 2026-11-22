import re
import tempfile
from pathlib import Path
from typing import BinaryIO

from .config import ALLOWED_EXTENSIONS, MAX_UPLOAD_BYTES
from .preprocessing import clean_text


class ResumeUploadError(ValueError):
    pass


def validate_resume(filename: str, size: int, content: bytes | None = None) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ResumeUploadError("Unsupported file type. Please upload a PDF or DOCX file.")
    if size <= 0:
        raise ResumeUploadError("The uploaded file is empty.")
    if size > MAX_UPLOAD_BYTES:
        raise ResumeUploadError("The uploaded file exceeds the 5 MB size limit.")
    if content is not None:
        if suffix == ".pdf" and not content.startswith(b"%PDF-"):
            raise ResumeUploadError("The file does not contain a valid PDF signature.")
        if suffix == ".docx" and not content.startswith(b"PK"):
            raise ResumeUploadError("The file does not contain a valid DOCX signature.")
    return suffix


def extract_pdf_text(path: Path) -> str:
    try:
        import fitz
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError as exc:
            raise ResumeUploadError("A PDF parser dependency is not installed.") from exc
        try:
            reader = PdfReader(str(path))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            raise ResumeUploadError("The PDF is corrupted or unreadable.") from exc

    try:
        document = fitz.open(str(path))
        if document.is_encrypted:
            document.close()
            raise ResumeUploadError("Encrypted PDF files are not supported.")
        text = "\n".join(page.get_text() for page in document)
        document.close()
        if not text.strip():
            raise ResumeUploadError("No readable text was found in the PDF.")
        return text
    except ResumeUploadError:
        raise
    except Exception as exc:
        raise ResumeUploadError("The PDF is corrupted or unreadable.") from exc


def extract_docx_text(path: Path) -> str:
    try:
        from docx import Document
        document = Document(str(path))
        parts = [p.text for p in document.paragraphs]
        for table in document.tables:
            for row in table.rows:
                parts.append(" | ".join(cell.text for cell in row.cells))
        text = "\n".join(parts)
        if not text.strip():
            raise ResumeUploadError("No readable text was found in the DOCX file.")
        return text
    except ResumeUploadError:
        raise
    except Exception as exc:
        raise ResumeUploadError("The DOCX file is corrupted or unreadable.") from exc


def extract_resume_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return extract_pdf_text(path).strip()
    if path.suffix.lower() == ".docx":
        return extract_docx_text(path).strip()
    raise ResumeUploadError("Unsupported resume format.")


def extract_contact_info(text: str) -> dict:
    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    phone_match = re.search(r"(?:\+\d{1,3}[-\s]?)?(?:\(?\d{2,4}\)?[-\s]?)\d{3,4}[-\s]?\d{3,4}", text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    name = ""
    if lines:
        candidate = lines[0]
        if len(candidate.split()) <= 5 and not any(char.isdigit() for char in candidate):
            name = candidate
    linkedin_match = re.search(r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?", text, re.I)
    github_match = re.search(r"https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+/?", text, re.I)
    portfolio_matches = re.findall(r"https?://(?!(?:www\.)?(?:linkedin\.com|github\.com))[A-Za-z0-9.-]+(?:/[A-Za-z0-9._~/?#=&%-]*)?", text, re.I)
    return {
        "name": name,
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0) if phone_match else "",
        "linkedin": linkedin_match.group(0) if linkedin_match else "",
        "github": github_match.group(0) if github_match else "",
        "portfolio": portfolio_matches[0] if portfolio_matches else "",
    }


def extract_sections(text: str) -> dict:
    section_names = (
        "summary", "professional summary", "profile", "objective",
        "experience", "work experience", "employment", "employment history",
        "education", "skills", "technical skills", "projects", "certifications",
    )
    heading_re = re.compile(r"(?im)^\s*(" + "|".join(re.escape(name) for name in sorted(section_names, key=len, reverse=True)) + r")\s*:?\s*$")
    matches = list(heading_re.finditer(text))
    sections = {}
    if not matches:
        return sections
    for index, match in enumerate(matches):
        heading = re.sub(r"[^a-z ]", "", match.group(1).lower()).strip()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[heading] = clean_text(text[match.end():end])
    return sections


def parse_resume(path: Path) -> dict:
    if not path.exists():
        raise ResumeUploadError("Resume file was not found.")
    text = extract_resume_text(path)
    return {
        "text": text,
        "contact": extract_contact_info(text),
        "sections": extract_sections(text),
    }
