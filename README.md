# AI RESUME ANALYZER

**AI RESUME ANALYZER** is a local-first Streamlit application that compares a PDF or DOCX resume against a job description and produces an explainable compatibility analysis. Its light workspace, charcoal navigation, and violet accents carry through the analysis dashboard and downloadable PDF report.

## Product areas

- Responsive SaaS interface with dashboard, guided upload, results, skill-gap, improvement, recommendation, comparison, and history views
- Real SQLite analysis history, searchable and sortable by role or score
- PDF/DOCX resume parsing with contact and section extraction
- Mandatory/preferred skill matching with evidence-aware catalog matching
- TF-IDF and optional local Sentence Transformers semantic relevance
- ATS-style keyword coverage (clearly distinguished from employer ATS scores)
- Prioritized skill gaps and resume-section improvements
- Skill-based role recommendations
- Previous/current resume comparison
- Multi-page professional PDF reports
- Privacy controls and temporary-file cleanup

## Architecture

```text
app.py                     Streamlit presentation and application orchestration
src/resume_parser.py       PDF/DOCX parsing and contact/section extraction
src/skill_extractor.py     Configurable skill taxonomy and evidence extraction
src/job_analyzer.py        Job title, qualification, skill, and experience analysis
src/matching_engine.py     TF-IDF and skill/experience calculations
src/semantic_matcher.py    Local embedding similarity with TF-IDF fallback
src/ats_analyzer.py        Keyword coverage and skill-gap construction
src/scoring_engine.py      Reproducible weighted scoring
src/recommendation_engine.py Evidence-based recommendations
src/database.py            Privacy-minimized SQLite persistence
src/report_generator.py    Branded multi-page ReportLab PDF output
ui/application.py          Streamlit navigation and page presentation
ui/theme.py                Shared Streamlit branding and metric components
assets/styles.css          Responsive charcoal, violet, and light-surface design system
.streamlit/config.toml     Light theme defaults and 5 MB upload limit
```

## Installation

Requirements: Python 3.11 or 3.12.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit.

## Scoring model

| Component | Weight | Method |
|---|---:|---|
| Skill match | 35% | Mandatory skills receive 80% of the skill component; preferred skills receive 20% |
| JD relevance | 25% | Combined semantic cosine similarity with TF-IDF fallback |
| Experience relevance | 15% | Resume experience years compared with detected JD requirement |
| Resume completeness | 15% | Presence of standard resume sections |
| Readability | 10% | Length, formatting, bullet, and action-verb heuristics |

The result is an estimated compatibility score. It is not an actual Workday, Greenhouse, Lever, or other employer ATS score and does not predict hiring or interview success.

## Privacy and storage

Resume files are written temporarily under `uploads/` and deleted after parsing or on exception. Report PDFs are generated under `reports/`. SQLite stores the job title, analysis date, compatibility/component scores, description hash, keywords, and skill status. It does not store resume text, resume files, or unnecessarily extracted candidate personal information.

Sentence Transformers may download `all-MiniLM-L6-v2` on first use. Once cached, matching can operate without another download. Hosted Streamlit deployments have their own hosting and filesystem privacy model; local-only guarantees should not be assumed.

## Testing

```powershell
pytest -q
```

## Usage

1. Select **New Analysis** from the workspace navigation.
2. Upload a PDF or DOCX resume (maximum 5 MB).
3. Enter or paste the target job description and optional title/company.
4. Review the compatibility score, score components, skill gaps, resume suggestions, and role recommendations.
5. Download the PDF report.

## Known limitations

- Image-only or scanned PDFs require OCR and are not automatically converted.
- Skill extraction is dictionary/context assisted and may miss uncommon or highly specialized terminology.
- Semantic similarity measures textual/contextual relationship, not demonstrated expertise.
- Role recommendations use skill overlap and are not career or hiring predictions.
- SQLite is suitable for local use and ephemeral hosting; production persistence needs durable storage.

## Deployment

Pin the Python and package versions, provide a writable `data/` directory, and configure durable storage before multi-user deployment. Streamlit Community Cloud restarts may clear SQLite and uploaded/report directories. A production deployment should use managed database/storage and an appropriate privacy/data-retention policy.
