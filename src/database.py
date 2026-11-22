import json
import sqlite3
from pathlib import Path

from .config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(path: Path | None = None) -> None:
    db_path = path or DATABASE_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            job_title TEXT,
            overall_score REAL,
            textual_relevance REAL,
            skill_match REAL,
            experience_relevance REAL,
            completeness_score REAL,
            readability_score REAL,
            report_path TEXT
        );

        CREATE TABLE IF NOT EXISTS job_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER NOT NULL,
            description_text_hash TEXT,
            required_skills_json TEXT,
            preferred_skills_json TEXT,
            experience_requirement TEXT,
            keywords_json TEXT,
            FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS skill_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER NOT NULL,
            skill_name TEXT,
            skill_category TEXT,
            status TEXT,
            requirement_type TEXT,
            FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
        );
        """)
        connection.execute("PRAGMA foreign_keys = ON")
        analysis_columns = {row[1] for row in connection.execute("PRAGMA table_info(analyses)").fetchall()}
        if "job_title" not in analysis_columns:
            connection.execute("ALTER TABLE analyses ADD COLUMN job_title TEXT")
        connection.commit()
    finally:
        connection.close()


def save_analysis(result: dict, path: Path | None = None) -> int:
    db_path = path or DATABASE_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    initialize_database(db_path)
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.execute("""
            INSERT INTO analyses
            (job_title, overall_score, textual_relevance,
             skill_match, experience_relevance, completeness_score, readability_score, report_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result["job"].get("job_title", "Not specified") or "Not specified",
            result["scores"].get("overall"),
            result["scores"].get("text_relevance"),
            result["scores"].get("skill_match"),
            result["scores"].get("experience_relevance"),
            result["scores"].get("completeness"),
            result["scores"].get("readability"),
            result.get("report_path"),
        ))
        analysis_id = cursor.lastrowid
        job = result["job"]
        connection.execute("""
            INSERT INTO job_descriptions
            (analysis_id, description_text_hash, required_skills_json,
             preferred_skills_json, experience_requirement, keywords_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            analysis_id, job.get("description_hash", ""),
            json.dumps(job.get("required_skills", [])),
            json.dumps(job.get("preferred_skills", [])),
            job.get("experience_requirement", ""),
            json.dumps(job.get("keywords", [])),
        ))

        skill_result = result["skill_match"]
        rows = []
        for skill in skill_result["required_matches"]:
            rows.append((analysis_id, skill, "", "matched", "required"))
        for skill in skill_result["required_missing"]:
            rows.append((analysis_id, skill, "", "missing", "required"))
        for skill in skill_result["preferred_matches"]:
            rows.append((analysis_id, skill, "", "matched", "preferred"))
        for skill in skill_result["preferred_missing"]:
            rows.append((analysis_id, skill, "", "missing", "preferred"))
        connection.executemany("""
            INSERT INTO skill_analysis
            (analysis_id, skill_name, skill_category, status, requirement_type)
            VALUES (?, ?, ?, ?, ?)
        """, rows)
        connection.commit()
        return int(analysis_id)
    finally:
        connection.close()


def list_analyses(path: Path | None = None) -> list[dict]:
    db_path = path or DATABASE_PATH
    initialize_database(db_path)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute("SELECT * FROM analyses ORDER BY created_at DESC, id DESC").fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def get_analysis(analysis_id: int, path: Path | None = None) -> dict:
    db_path = path or DATABASE_PATH
    initialize_database(db_path)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        analysis = connection.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,)).fetchone()
        if analysis is None:
            raise KeyError(f"Analysis {analysis_id} was not found")
        job = connection.execute("SELECT * FROM job_descriptions WHERE analysis_id = ?", (analysis_id,)).fetchone()
        skills = connection.execute("SELECT * FROM skill_analysis WHERE analysis_id = ? ORDER BY skill_name", (analysis_id,)).fetchall()
        return {
            "analysis": dict(analysis),
            "job": dict(job) if job else None,
            "skills": [dict(row) for row in skills],
        }
    finally:
        connection.close()


def delete_analysis(analysis_id: int, path: Path | None = None) -> None:
    db_path = path or DATABASE_PATH
    connection = sqlite3.connect(db_path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
        connection.execute("DELETE FROM job_descriptions WHERE analysis_id = ?", (analysis_id,))
        connection.execute("DELETE FROM skill_analysis WHERE analysis_id = ?", (analysis_id,))
        connection.commit()
    finally:
        connection.close()


def delete_all_analyses(path: Path | None = None) -> None:
    db_path = path or DATABASE_PATH
    connection = sqlite3.connect(db_path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("DELETE FROM skill_analysis")
        connection.execute("DELETE FROM job_descriptions")
        connection.execute("DELETE FROM analyses")
        connection.commit()
    finally:
        connection.close()
