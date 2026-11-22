from html import escape
from pathlib import Path
import uuid

import pandas as pd
import streamlit as st

from src.database import (
    delete_all_analyses,
    delete_analysis,
    get_analysis,
    list_analyses,
)
from src.matching_engine import calculate_skill_match
from src.resume_parser import parse_resume, validate_resume
from src.skill_extractor import SKILL_CATALOG, extract_skills
from src.config import UPLOAD_DIR
from ui.theme import logo, progress_bar, render_metric


NAV_ITEMS = {
    "⌂  Dashboard": "Dashboard",
    "＋  New Analysis": "New Analysis",
    "◈  Analysis Results": "Analysis Results",
    "◎  Skill Gap Analysis": "Skill Gap",
    "✧  Resume Improvement": "Resume Improvement",
    "↗  Job Recommendations": "Job Recommendations",
    "⇄  Resume Comparison": "Resume Comparison",
    "◷  Analysis History": "Analysis History",
    "⚙  Settings": "Settings",
}


def _navigate(label: str) -> None:
    st.session_state["pending_navigation"] = label
    st.rerun()


def _page_header(title: str, description: str) -> None:
    st.markdown(
        f"<div class='page-heading'><div><div class='eyebrow'>AI RESUME ANALYZER</div>"
        f"<h1>{escape(title)}</h1><p>{escape(description)}</p></div></div>",
        unsafe_allow_html=True,
    )


def _empty_state(title: str, message: str, action: str | None = None) -> None:
    st.markdown(
        f"<div class='empty-state'><div class='empty-mark'>✦</div>"
        f"<strong>{escape(title)}</strong><p>{escape(message)}</p></div>",
        unsafe_allow_html=True,
    )
    if action and st.button(action, type="primary"):
        _navigate("＋  New Analysis")


def _skill_pills(
    skills: list[str], tone: str, empty_text: str = "None identified"
) -> str:
    if not skills:
        return f"<span class='muted-copy'>{escape(empty_text)}</span>"
    return "".join(
        f"<span class='skill-pill {tone}'>{escape(str(skill))}</span>"
        for skill in skills
    )


def _format_date(value: str | None) -> str:
    if not value:
        return "Date unavailable"
    return escape(str(value)[:16].replace("T", " "))


def _related_skills(skill: str, resume_skills: dict) -> list[str]:
    for category, catalog in SKILL_CATALOG.items():
        if skill in catalog:
            return [
                item
                for item in resume_skills.get("categories", {}).get(category, [])
                if item != skill
            ]
    return []


def _history_details(analysis_id: int) -> None:
    detail = get_analysis(analysis_id)
    record = detail["analysis"]
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='section-heading'><div><div class='eyebrow'>SAVED ANALYSIS</div>"
        f"<h2>{escape(record.get('job_title') or 'Untitled analysis')}</h2>"
        f"<p>{_format_date(record.get('created_at'))}</p></div>"
        f"<div class='history-score'>{(record.get('overall_score') or 0):.0f}<span>%</span></div></div>",
        unsafe_allow_html=True,
    )
    score_items = [
        ("Skill match", record.get("skill_match") or 0),
        ("Job relevance", record.get("textual_relevance") or 0),
        ("Experience", record.get("experience_relevance") or 0),
        ("Completeness", record.get("completeness_score") or 0),
        ("Readability", record.get("readability_score") or 0),
    ]
    score_columns = st.columns(5)
    for column, (label, score) in zip(score_columns, score_items):
        column.markdown(
            render_metric(label, f"{score:.0f}%", "saved score"),
            unsafe_allow_html=True,
        )

    skills = detail["skills"]
    groups = [
        (
            "Matched mandatory",
            [
                item["skill_name"]
                for item in skills
                if item["status"] == "matched" and item["requirement_type"] == "required"
            ],
            "success",
        ),
        (
            "Missing mandatory",
            [
                item["skill_name"]
                for item in skills
                if item["status"] == "missing" and item["requirement_type"] == "required"
            ],
            "danger",
        ),
        (
            "Matched preferred",
            [
                item["skill_name"]
                for item in skills
                if item["status"] == "matched" and item["requirement_type"] == "preferred"
            ],
            "success",
        ),
        (
            "Missing preferred",
            [
                item["skill_name"]
                for item in skills
                if item["status"] == "missing" and item["requirement_type"] == "preferred"
            ],
            "warning",
        ),
    ]
    st.markdown("#### Skill comparison")
    skill_columns = st.columns(4)
    for column, (heading, values, tone) in zip(skill_columns, groups):
        column.markdown(
            f"<div class='card skill-group'><strong>{heading}</strong><div class='skill-list'>"
            f"{_skill_pills(values, tone)}</div></div>",
            unsafe_allow_html=True,
        )
    if not skills:
        st.caption("No skill-level details were saved for this analysis.")


def _dashboard() -> None:
    history = list_analyses()
    average = (
        round(sum(record["overall_score"] or 0 for record in history) / len(history), 1)
        if history
        else None
    )
    matched_count = 0
    missing_count = 0
    if history:
        latest_detail = get_analysis(int(history[0]["id"]))
        matched_count = sum(
            1 for row in latest_detail["skills"] if row["status"] == "matched"
        )
        missing_count = sum(
            1 for row in latest_detail["skills"] if row["status"] == "missing"
        )

    st.markdown(
        "<div class='hero'><div class='hero-copy'><div class='eyebrow'>AI RESUME ANALYZER · YOUR CAREER WORKSPACE</div>"
        "<h1>Make your next move<br>with confidence.</h1>"
        "<p>Understand how your experience aligns with the role, then turn the insight into a stronger application.</p>"
        "</div><div class='hero-orbit'><span>✦</span><i></i><b></b></div></div>",
        unsafe_allow_html=True,
    )
    hero_action, hero_note = st.columns([1, 4])
    with hero_action:
        if st.button("＋  Start new analysis", type="primary", use_container_width=True):
            _navigate("＋  New Analysis")
    with hero_note:
        st.markdown(
            "<div class='hero-note'>Evidence-based matching &nbsp;·&nbsp; "
            "Private local processing &nbsp;·&nbsp; Clear next steps</div>",
            unsafe_allow_html=True,
        )

    empty_detail = "Run your first analysis to see this metric."
    columns = st.columns(4)
    metrics = [
        ("Total analyses", str(len(history)), "saved in your workspace"),
        (
            "Average match",
            f"{average:.1f}%" if average is not None else "—",
            "across saved analyses" if history else empty_detail,
        ),
        (
            "Strong skill matches",
            str(matched_count),
            "latest saved analysis" if history else empty_detail,
        ),
        (
            "Missing skills",
            str(missing_count),
            "latest saved analysis" if history else empty_detail,
        ),
    ]
    for column, (label, value, detail) in zip(columns, metrics):
        column.markdown(
            render_metric(label, value, detail),
            unsafe_allow_html=True,
        )

    activity_col, insight_col = st.columns([1.35, 1])
    with activity_col:
        st.markdown(
            "<div class='section-heading compact'><div><div class='eyebrow'>YOUR WORKSPACE</div>"
            "<h2>Recent activity</h2></div></div>",
            unsafe_allow_html=True,
        )
        if history:
            for record in history[:5]:
                row_title = escape(record.get("job_title") or "Untitled analysis")
                score = record.get("overall_score") or 0
                activity_a, activity_b, activity_c = st.columns([3, 1.1, 1.1])
                activity_a.markdown(
                    f"<div class='activity-title'>{row_title}</div>"
                    f"<div class='activity-date'>{_format_date(record.get('created_at'))}</div>",
                    unsafe_allow_html=True,
                )
                activity_b.markdown(
                    f"<div class='activity-score'>{score:.0f}<span>%</span></div>",
                    unsafe_allow_html=True,
                )
                if activity_c.button("View", key=f"dashboard_view_{record['id']}"):
                    st.session_state["history_selected_id"] = int(record["id"])
                    _navigate("◷  Analysis History")
                st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)
        else:
            _empty_state(
                "Your history starts here",
                "Completed resume analyses will appear here with their scores and skill breakdown.",
                "Create your first analysis",
            )
    with insight_col:
        st.markdown(
            "<div class='section-heading compact'><div><div class='eyebrow'>AT A GLANCE</div>"
            "<h2>Latest score profile</h2></div></div>",
            unsafe_allow_html=True,
        )
        if history:
            latest = history[0]
            st.markdown(
                f"<div class='card chart-card'><div class='chart-card-head'>"
                f"<span>{escape(latest.get('job_title') or 'Latest analysis')}</span>"
                f"<strong>{(latest.get('overall_score') or 0):.0f}%</strong></div></div>",
                unsafe_allow_html=True,
            )
            chart_data = pd.DataFrame(
                {
                    "Component": [
                        "Skills",
                        "Role relevance",
                        "Experience",
                        "Completeness",
                        "Readability",
                    ],
                    "Score": [
                        latest.get("skill_match") or 0,
                        latest.get("textual_relevance") or 0,
                        latest.get("experience_relevance") or 0,
                        latest.get("completeness_score") or 0,
                        latest.get("readability_score") or 0,
                    ],
                }
            ).set_index("Component")
            st.bar_chart(chart_data, height=220, color="#635BFF")
        else:
            _empty_state(
                "Insights appear after analysis",
                "Your charts use real component scores from your saved results.",
            )

    st.markdown(
        "<div class='section-heading compact'><div><div class='eyebrow'>BUILT FOR YOUR NEXT STEP</div>"
        "<h2>Explore your tools</h2></div></div>",
        unsafe_allow_html=True,
    )
    tools = [
        ("◈", "Role alignment", "See match scores and the evidence behind them."),
        ("◎", "Skill gaps", "Prioritize the qualifications to build next."),
        ("✧", "Resume improvement", "Get section-by-section suggestions."),
        ("⇄", "Version comparison", "See which skills changed between drafts."),
    ]
    tool_columns = st.columns(4)
    for column, (icon, title, description) in zip(tool_columns, tools):
        column.markdown(
            f"<div class='card tool-card'><div class='tool-icon'>{icon}</div>"
            f"<h3>{title}</h3><p>{description}</p></div>",
            unsafe_allow_html=True,
        )


def _new_analysis(run_analysis, sample_jd: str, upload_error: type[Exception]) -> None:
    _page_header(
        "New analysis",
        "Compare your resume with a role to surface clear, evidence-based next steps.",
    )
    st.markdown(
        "<div class='privacy-banner'><span class='status-dot'></span>"
        "<span>Your resume is processed locally and the uploaded file is removed after analysis.</span></div>",
        unsafe_allow_html=True,
    )
    upload_col, jd_col = st.columns([1, 1.15])
    with upload_col:
        st.markdown(
            "<div class='section-heading compact'><div><div class='eyebrow'>STEP 01</div>"
            "<h2>Your resume</h2></div></div>",
            unsafe_allow_html=True,
        )
        uploader_key = f"main_resume_{st.session_state.get('resume_uploader_version', 0)}"
        uploaded = st.file_uploader(
            "Upload a PDF or DOCX",
            type=["pdf", "docx"],
            key=uploader_key,
            help="Maximum file size: 5 MB.",
        )
        upload_valid = False
        if uploaded:
            try:
                validate_resume(uploaded.name, uploaded.size, uploaded.getvalue())
                upload_valid = True
                file_type = escape(Path(uploaded.name).suffix[1:].upper())
                st.markdown(
                    f"<div class='file-card'><div class='file-icon'>{file_type}</div><div class='file-info'>"
                    f"<strong>{escape(uploaded.name)}</strong><span>{uploaded.size / 1024:.1f} KB · "
                    f"{escape(uploaded.type or 'Document')}</span></div>"
                    "<span class='file-status'>Ready</span></div>",
                    unsafe_allow_html=True,
                )
            except upload_error as exc:
                st.error(str(exc))
            remove_col, replace_col = st.columns(2)
            if remove_col.button("Remove file", use_container_width=True):
                st.session_state["resume_uploader_version"] = (
                    st.session_state.get("resume_uploader_version", 0) + 1
                )
                st.rerun()
            if replace_col.button("Replace file", use_container_width=True):
                st.session_state["resume_uploader_version"] = (
                    st.session_state.get("resume_uploader_version", 0) + 1
                )
                st.rerun()
        else:
            st.markdown(
                "<div class='upload-hint'><div class='upload-symbol'>↑</div>"
                "<strong>Drop your resume here</strong><span>PDF or DOCX · up to 5 MB</span></div>",
                unsafe_allow_html=True,
            )
        st.markdown(
            "<div class='helper-card'><strong>What happens to my file?</strong>"
            "<p>We extract text for this analysis, then remove the uploaded file. "
            "Saved history contains scores and skill status, not resume text.</p></div>",
            unsafe_allow_html=True,
        )

    with jd_col:
        st.markdown(
            "<div class='section-heading compact'><div><div class='eyebrow'>STEP 02</div>"
            "<h2>Target role</h2></div></div>",
            unsafe_allow_html=True,
        )
        job_title = st.text_input("Job title", placeholder="e.g. Senior Python Developer")
        company = st.text_input("Company (optional)", placeholder="Company name")
        jd_version = st.session_state.get("job_description_version", 0)
        job_description_key = f"job_description_{jd_version}"
        if "pending_job_description" in st.session_state:
            st.session_state[job_description_key] = st.session_state.pop(
                "pending_job_description"
            )
        job_text = st.text_area(
            "Job description",
            height=250,
            key=job_description_key,
            placeholder="Paste the role responsibilities, qualifications, and preferred skills...",
            help="Include the full description for a more useful comparison.",
        )
        count_col, clear_col, sample_col = st.columns([1.5, 1, 1])
        count_col.caption(f"{len(job_text):,} characters")
        if clear_col.button("Clear", use_container_width=True):
            st.session_state["pending_job_description"] = ""
            st.rerun()
        if sample_col.button("Use sample", use_container_width=True):
            st.session_state["pending_job_description"] = sample_jd
            st.rerun()

    if st.button("Analyze resume  →", type="primary", use_container_width=True):
        if uploaded is None:
            st.error("Please upload a PDF or DOCX resume.")
        elif not upload_valid:
            st.error("Please replace the selected file with a valid PDF or DOCX resume.")
        elif len(job_text.strip()) < 20:
            st.error(
                "Please enter a job description containing at least 20 characters to run a useful comparison."
            )
        else:
            with st.spinner("Parsing resume and generating explainable analysis..."):
                try:
                    result = run_analysis(uploaded, job_text, job_title, company)
                    st.session_state["analysis_result"] = result
                    st.success("Analysis complete. Your results are ready.")
                    _navigate("◈  Analysis Results")
                except (upload_error, ValueError) as exc:
                    st.error(str(exc))


def _analysis_results() -> None:
    result = st.session_state.get("analysis_result")
    if not result:
        _page_header(
            "Analysis results",
            "A clear view of your alignment, strengths, and opportunity areas.",
        )
        _empty_state(
            "No active results yet",
            "Run a resume analysis to see your compatibility score and skill comparison.",
            "Start a new analysis",
        )
        return

    scores = result["scores"]
    label, tone = _classification(scores["overall"])
    role_title = result["job"].get("job_title") or "Resume and role comparison"
    _page_header(
        "Analysis results",
        f"{role_title} · Evidence-based compatibility insights",
    )
    top1, top2 = st.columns([0.9, 1.6])
    with top1:
        st.markdown(
            f"<div class='card score-card'><div class='eyebrow'>OVERALL COMPATIBILITY</div>"
            f"<div class='score-ring' style='--score:{scores['overall']:.0f}%'>"
            f"<div class='score-ring-inner'><div><strong>{scores['overall']:.0f}"
            f"<small>%</small></strong><span>Match score</span></div></div></div>"
            f"<span class='status-pill {tone}'>{escape(label)}</span>"
            "<p>Estimated alignment from the scoring components and skill evidence below.</p></div>",
            unsafe_allow_html=True,
        )
    with top2:
        st.markdown(
            "<div class='card breakdown-card'><div class='eyebrow'>HOW THE SCORE IS BUILT</div>"
            "<h2>Score breakdown</h2>",
            unsafe_allow_html=True,
        )
        items = [
            ("Skill match", scores["skill_match"], "35% of score"),
            ("Job relevance", scores["text_relevance"], "25% of score"),
            ("Experience relevance", scores["experience_relevance"], "15% of score"),
            ("Resume completeness", scores["completeness"], "15% of score"),
            ("Readability", scores["readability"], "10% of score"),
        ]
        for name, value, detail in items:
            st.markdown(
                f"<div class='score-row'><div class='score-row-head'><strong>{name}</strong>"
                f"<span>{value:.0f}% <small>{detail}</small></span></div>{progress_bar(value)}</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    skill_match = result["skill_match"]
    st.markdown(
        "<div class='section-heading'><div><div class='eyebrow'>CAPABILITY MATCH</div>"
        "<h2>Skills comparison</h2><p>Required and preferred skills detected in the resume and job description.</p></div></div>",
        unsafe_allow_html=True,
    )
    groups = [
        ("Matched mandatory", skill_match["required_matches"], "success", "In your resume"),
        ("Missing mandatory", skill_match["required_missing"], "danger", "Priority gap"),
        ("Matched preferred", skill_match["preferred_matches"], "success", "In your resume"),
        ("Missing preferred", skill_match["preferred_missing"], "warning", "Growth area"),
    ]
    for column, (title, skills, tone, helper) in zip(st.columns(4, gap="medium"), groups):
        column.markdown(
            f"<div class='card skill-group'><div class='skill-group-head'>"
            f"<strong>{title}</strong><span class='group-count'>{len(skills)}</span></div>"
            f"<p>{helper}</p><div class='skill-list'>{_skill_pills(skills, tone)}</div></div>",
            unsafe_allow_html=True,
        )

    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.markdown(
            "<div class='section-heading compact'><div><div class='eyebrow'>SCORE PROFILE</div>"
            "<h2>Compatibility breakdown</h2></div></div>",
            unsafe_allow_html=True,
        )
        breakdown = pd.DataFrame(
            {
                "Component": [
                    "Skills",
                    "Job relevance",
                    "Experience",
                    "Completeness",
                    "Readability",
                ],
                "Score": [
                    scores["skill_match"],
                    scores["text_relevance"],
                    scores["experience_relevance"],
                    scores["completeness"],
                    scores["readability"],
                ],
            }
        ).set_index("Component")
        st.bar_chart(breakdown, height=250, color="#635BFF")
    with chart_right:
        st.markdown(
            "<div class='section-heading compact'><div><div class='eyebrow'>KEYWORD SIGNAL</div>"
            "<h2>Job keyword coverage</h2></div></div>",
            unsafe_allow_html=True,
        )
        ats = result["ats_analysis"]
        keyword_chart = pd.DataFrame(
            {
                "Status": ["Found in resume", "Not found"],
                "Count": [len(ats["matched"]), len(ats["missing"])],
            }
        ).set_index("Status")
        st.bar_chart(keyword_chart, height=250, color="#8B7CFF")

    st.markdown(
        "<div class='section-heading compact'><div><div class='eyebrow'>ADDITIONAL SIGNALS</div>"
        "<h2>Keyword insights</h2></div></div>",
        unsafe_allow_html=True,
    )
    insight_columns = st.columns(3)
    insights = [
        (
            "Keyword coverage",
            f"{ats['score']}%",
            "Keyword signal only · not an employer ATS score",
        ),
        ("Matched keywords", str(len(ats["matched"])), "identified in resume and role"),
        (
            "Mandatory gaps",
            str(len(skill_match["required_missing"])),
            "required skills not detected",
        ),
    ]
    for column, values in zip(insight_columns, insights):
        column.markdown(render_metric(*values), unsafe_allow_html=True)

    keyword_col, recommendation_col = st.columns([1, 1])
    with keyword_col:
        st.markdown(
            "<div class='section-heading compact'><div><div class='eyebrow'>ROLE LANGUAGE</div>"
            "<h2>Matched keywords</h2></div></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='card keyword-card'>{_skill_pills(ats['matched'][:20], 'success')}</div>",
            unsafe_allow_html=True,
        )
    with recommendation_col:
        st.markdown(
            "<div class='section-heading compact'><div><div class='eyebrow'>NEXT STEPS</div>"
            "<h2>Top recommendations</h2></div></div>",
            unsafe_allow_html=True,
        )
        if result["recommendations"]:
            for recommendation in result["recommendations"][:3]:
                st.markdown(
                    f"<div class='recommendation-row'><span>✦</span><p>{escape(recommendation)}</p></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No additional recommendations were generated.")

    report_path = Path(result["report_path"])
    if report_path.exists():
        st.download_button(
            "↓  Download branded PDF report",
            data=report_path.read_bytes(),
            file_name=report_path.name,
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.error("The PDF report could not be found. Run the analysis again to generate a new report.")


def _classification(score: float) -> tuple[str, str]:
    if score >= 80:
        return "Strong alignment", "success"
    if score >= 60:
        return "Moderate alignment", "warning"
    return "Needs development", "danger"


def _skill_gap() -> None:
    _page_header(
        "Skill gap analysis",
        "Prioritize the missing qualifications that matter most for this role.",
    )
    result = st.session_state.get("analysis_result")
    if not result:
        _empty_state(
            "No active skill gaps",
            "Run an analysis first. Skill priorities are based on the role requirements you provide.",
            "Start a new analysis",
        )
        return
    if not result["skill_gaps"]:
        st.markdown(
            "<div class='success-panel'><div class='success-icon'>✓</div><div>"
            "<strong>No missing skills detected</strong><p>Every catalog skill identified in this role was also detected in your resume.</p></div></div>",
            unsafe_allow_html=True,
        )
        return

    mandatory_count = sum(
        gap["importance"] == "Mandatory" for gap in result["skill_gaps"]
    )
    preferred_count = len(result["skill_gaps"]) - mandatory_count
    gap_a, gap_b = st.columns(2)
    gap_a.markdown(
        render_metric(
            "Mandatory gaps",
            str(mandatory_count),
            "explicitly required in the job description",
        ),
        unsafe_allow_html=True,
    )
    gap_b.markdown(
        render_metric(
            "Preferred gaps",
            str(preferred_count),
            "additional capabilities that may help",
        ),
        unsafe_allow_html=True,
    )
    for gap in result["skill_gaps"]:
        mandatory = gap["importance"] == "Mandatory"
        tone = "danger" if mandatory else "warning"
        related_html = _skill_pills(
            _related_skills(gap["skill"], result["resume_skills"]),
            "neutral",
            "No related skill evidence detected",
        )
        topics = "".join(
            f"<span class='topic-chip'>{escape(topic)}</span>"
            for topic in gap["learning_topics"]
        )
        st.markdown(
            f"<div class='card gap-card'><div class='gap-head'><div>"
            f"<span class='status-pill {tone}'>"
            f"{'HIGH PRIORITY · REQUIRED' if mandatory else 'PREFERRED · OPTIONAL'}</span>"
            f"<h3>{escape(gap['skill'])}</h3></div>"
            f"<span class='priority-mark {tone}'>{'!' if mandatory else '↗'}</span></div>"
            f"<p>{escape(gap['why'])}</p><div class='gap-meta'>"
            f"<div><strong>Suggested learning topics</strong><div class='topic-list'>{topics}</div></div>"
            f"<div><strong>Related strengths in your resume</strong>"
            f"<div class='skill-list'>{related_html}</div></div></div></div>",
            unsafe_allow_html=True,
        )


def _resume_improvement() -> None:
    _page_header(
        "Resume improvement",
        "Actionable suggestions grounded in the sections and formatting detected in your resume.",
    )
    result = st.session_state.get("analysis_result")
    if not result:
        _empty_state(
            "Suggestions need a resume",
            "Analyze your resume to receive section-specific observations and improvements.",
            "Start a new analysis",
        )
        return

    section_aliases = {
        "Professional Summary": (
            "professional summary",
            "summary",
            "profile",
            "objective",
        ),
        "Technical Skills": ("technical skills", "skills"),
        "Work Experience": (
            "work experience",
            "experience",
            "employment",
            "employment history",
        ),
        "Projects": ("projects", "project experience"),
        "Education": ("education", "academic background"),
        "Certifications": ("certifications", "certificates", "licenses"),
    }
    section_order = [
        "Professional Summary",
        "Technical Skills",
        "Work Experience",
        "Projects",
        "Education",
        "Certifications",
    ]
    sections = section_order + [
        section
        for section in result["section_suggestions"]
        if section not in section_order
    ]
    for section in sections:
        suggestions = result["section_suggestions"].get(
            section,
            [
                "No specific issue was flagged. Keep this section accurate and emphasize the details most relevant to the target role."
            ],
        )
        aliases = section_aliases.get(section, (section.lower(),))
        current = next(
            (
                value
                for key, value in result["sections"].items()
                if key.lower() in aliases
            ),
            "",
        )
        observation = (
            f"Section detected · {len(current.split())} words"
            if current
            else "No dedicated section detected in the extracted resume."
        )
        excerpt = current.strip()
        if len(excerpt) > 500:
            excerpt = excerpt[:497].rsplit(" ", 1)[0] + "..."
        suggestion_html = "".join(
            f"<div class='suggestion-row'><span>✦</span><p>{escape(suggestion)}</p></div>"
            for suggestion in suggestions
        )
        excerpt_html = escape(excerpt) if excerpt else "No current section text available."
        st.markdown(
            f"<div class='card improvement-card'><div class='improvement-head'><div>"
            f"<div class='eyebrow'>RESUME SECTION</div><h3>{escape(section)}</h3></div>"
            f"<span class='observation-pill'>{escape(observation)}</span></div>"
            f"<div class='improvement-columns'><div class='current-observation'>"
            f"<strong>Current observation</strong><p>{excerpt_html}</p></div>"
            f"<div class='suggestion-block'><strong>Suggested improvements</strong>"
            f"{suggestion_html}</div></div></div>",
            unsafe_allow_html=True,
        )
    st.caption(
        "Suggestions are prompts for truthful improvements. Do not add experience, skills, or qualifications you do not have."
    )


def _job_recommendations() -> None:
    _page_header(
        "Job recommendations",
        "Explore roles based only on the skills identified in your resume.",
    )
    result = st.session_state.get("analysis_result")
    if not result:
        _empty_state(
            "No role matches yet",
            "Analyze a resume to see role suggestions based on demonstrated skill overlap.",
            "Start a new analysis",
        )
    elif not result["role_recommendations"]:
        _empty_state(
            "No catalog roles matched",
            "The current resume did not contain enough recognized skills to match a role in the catalog.",
        )
    else:
        role_columns = st.columns(2, gap="medium")
        for index, role in enumerate(result["role_recommendations"]):
            role_columns[index % 2].markdown(
                f"<div class='card role-card'><div class='role-card-head'>"
                f"<div class='tool-icon'>↗</div><span class='status-pill neutral'>"
                f"{role['coverage']:.0f}% overlap</span></div><h3>{escape(role['role'])}</h3>"
                f"<p>{escape(role['reason'])}</p>"
                f"<div class='skill-list'>{_skill_pills(role['evidence'], 'success')}</div></div>",
                unsafe_allow_html=True,
            )
        st.caption(
            "Role suggestions are based on catalog skill overlap, not a hiring prediction."
        )


def _resume_comparison(upload_error: type[Exception]) -> None:
    _page_header(
        "Resume comparison",
        "Compare detected skills between a previous resume and your current analysis.",
    )
    result = st.session_state.get("analysis_result")
    previous = st.file_uploader(
        "Upload previous resume version",
        type=["pdf", "docx"],
        key="comparison_resume",
    )
    if previous and result:
        previous_path = (
            UPLOAD_DIR
            / f"previous_{uuid.uuid4().hex}{Path(previous.name).suffix.lower()}"
        )
        try:
            validate_resume(previous.name, previous.size, previous.getvalue())
            previous_path.write_bytes(previous.getvalue())
            old_resume = parse_resume(previous_path)
            old_skills = set(extract_skills(old_resume["text"])["skills"])
            new_skills = set(result["resume_skills"]["skills"])
            old_match = calculate_skill_match(
                list(old_skills),
                result["job"]["required_skills"],
                result["job"]["preferred_skills"],
            )
            columns = st.columns(3)
            columns[0].markdown(
                render_metric(
                    "Previous skill match",
                    f"{old_match['skill_match_score']:.1f}%",
                    "previous resume",
                ),
                unsafe_allow_html=True,
            )
            columns[1].markdown(
                render_metric(
                    "Current skill match",
                    f"{result['skill_match']['skill_match_score']:.1f}%",
                    f"{result['skill_match']['skill_match_score'] - old_match['skill_match_score']:+.1f} pp",
                ),
                unsafe_allow_html=True,
            )
            columns[2].markdown(
                render_metric(
                    "Net skill change",
                    str(len(new_skills - old_skills) - len(old_skills - new_skills)),
                    "new minus removed",
                ),
                unsafe_allow_html=True,
            )
            added, removed = st.columns(2)
            added.markdown(
                f"<div class='card skill-group'><strong>Newly added skills</strong>"
                f"<div class='skill-list'>{_skill_pills(sorted(new_skills - old_skills), 'success')}</div></div>",
                unsafe_allow_html=True,
            )
            removed.markdown(
                f"<div class='card skill-group'><strong>Skills no longer detected</strong>"
                f"<div class='skill-list'>{_skill_pills(sorted(old_skills - new_skills), 'warning')}</div></div>",
                unsafe_allow_html=True,
            )
        except (upload_error, ValueError) as exc:
            st.error(str(exc))
        finally:
            if previous_path.exists():
                previous_path.unlink(missing_ok=True)
    elif not result:
        _empty_state(
            "Analyze a current resume first",
            "A completed analysis is needed as the current version for comparison.",
            "Start a new analysis",
        )
    else:
        st.markdown(
            "<div class='helper-card'><strong>Ready to compare</strong>"
            "<p>Upload an earlier PDF or DOCX to compare its detected skill set with the current analysis.</p></div>",
            unsafe_allow_html=True,
        )


def _history() -> None:
    _page_header(
        "Analysis history",
        "Review saved results and revisit skill-level details from previous comparisons.",
    )
    history = list_analyses()
    if not history:
        _empty_state(
            "No saved analyses",
            "Your completed analyses will appear here. Saved history excludes resume text and original files.",
            "Create your first analysis",
        )
        return

    search = st.text_input(
        "Search analyses",
        placeholder="Filter by job title",
        key="history_search",
    )
    filtered = (
        [
            record
            for record in history
            if search.lower() in (record.get("job_title") or "").lower()
        ]
        if search
        else history
    )
    filter_col, count_col = st.columns([3, 1])
    with filter_col:
        st.caption(f"Showing {len(filtered)} of {len(history)} saved analyses")
    with count_col:
        sort_choice = st.selectbox(
            "Sort",
            ["Newest first", "Highest score"],
            label_visibility="collapsed",
            key="history_sort",
        )
    if sort_choice == "Highest score":
        filtered = sorted(
            filtered,
            key=lambda item: item.get("overall_score") or 0,
            reverse=True,
        )
    if not filtered:
        _empty_state("No matching analyses", "Try another job title or clear your search.")
    for record in filtered:
        entry_left, entry_score, view_col, delete_col = st.columns([3, 1, 1, 1])
        entry_left.markdown(
            f"<div class='history-title'>{escape(record.get('job_title') or 'Untitled analysis')}</div>"
            f"<div class='activity-date'>{_format_date(record.get('created_at'))}</div>",
            unsafe_allow_html=True,
        )
        entry_score.markdown(
            f"<div class='activity-score large'>{(record.get('overall_score') or 0):.0f}"
            f"<span>%</span></div>",
            unsafe_allow_html=True,
        )
        if view_col.button("View", key=f"view_{record['id']}"):
            st.session_state["history_selected_id"] = int(record["id"])
            st.rerun()
        if delete_col.button("Delete", key=f"delete_{record['id']}"):
            delete_analysis(int(record["id"]))
            if st.session_state.get("history_selected_id") == int(record["id"]):
                st.session_state.pop("history_selected_id", None)
            st.toast("Analysis removed from saved history.")
            st.rerun()
        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

    selected_id = st.session_state.get("history_selected_id")
    if selected_id and any(int(record["id"]) == selected_id for record in history):
        _history_details(int(selected_id))


def _settings() -> None:
    _page_header(
        "Settings",
        "Understand how your data is handled and how the match score is calculated.",
    )
    st.markdown(
        "<div class='card settings-card'><div class='tool-icon'>◉</div><h3>Privacy & storage</h3>"
        "<p>Resume uploads are temporary and removed after processing. The local SQLite database stores "
        "analysis metadata, component scores, a job-description hash, and skill status—not resume text "
        "or original personal information.</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='card settings-card'><div class='tool-icon'>◈</div><h3>Scoring methodology</h3>"
        "<p><strong>Skill match 35%</strong> · Job relevance 25% · Experience relevance 15% · "
        "Completeness 15% · Readability 10%</p><p>This is an estimated compatibility score, "
        "not an employer ATS score or hiring prediction.</p></div>",
        unsafe_allow_html=True,
    )
    if st.button("Delete all saved history", type="secondary"):
        delete_all_analyses()
        st.session_state.pop("history_selected_id", None)
        st.success("All saved analysis history was deleted.")


def render_application(run_analysis, sample_jd: str, upload_error: type[Exception]) -> None:
    if "pending_navigation" in st.session_state:
        st.session_state["navigation"] = st.session_state.pop("pending_navigation")
    current_navigation = st.session_state.get("navigation")
    if current_navigation not in NAV_ITEMS:
        st.session_state["navigation"] = next(iter(NAV_ITEMS))

    with st.sidebar:
        st.markdown(logo(), unsafe_allow_html=True)
        st.markdown("<div class='sidebar-label'>WORKSPACE</div>", unsafe_allow_html=True)
        page_choice = st.radio(
            "Workspace",
            list(NAV_ITEMS.keys()),
            key="navigation",
            label_visibility="collapsed",
        )
        page = NAV_ITEMS[page_choice]
        st.markdown(
            "<div class='sidebar-footer'><span class='status-dot'></span>"
            "<strong>Private by design</strong><p>Resume files are removed after analysis. "
            "History stores scores and skill status only.</p></div>",
            unsafe_allow_html=True,
        )

    if page == "Dashboard":
        _dashboard()
    elif page == "New Analysis":
        _new_analysis(run_analysis, sample_jd, upload_error)
    elif page == "Analysis Results":
        _analysis_results()
    elif page == "Skill Gap":
        _skill_gap()
    elif page == "Resume Improvement":
        _resume_improvement()
    elif page == "Job Recommendations":
        _job_recommendations()
    elif page == "Resume Comparison":
        _resume_comparison(upload_error)
    elif page == "Analysis History":
        _history()
    elif page == "Settings":
        _settings()

    st.markdown(
        "<div class='app-footer'>AI RESUME ANALYZER <span>·</span> "
        "Thoughtful insights for your next opportunity</div>",
        unsafe_allow_html=True,
    )
