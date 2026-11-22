from datetime import datetime
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from .config import REPORT_DIR


INK = colors.HexColor("#09090B")
VIOLET = colors.HexColor("#635BFF")
LAVENDER = colors.HexColor("#F0EFFF")
MUTED = colors.HexColor("#777B8B")
LINE = colors.HexColor("#E7E8EE")
PALE = colors.HexColor("#F5F6FA")


def generate_pdf_report(result: dict, output_path: Path | None = None) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    if output_path is None:
        analysis_id = result.get("analysis_id", "new")
        output_path = REPORT_DIR / f"resume_analysis_{analysis_id}.pdf"

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=48,
        leftMargin=48,
        topMargin=68,
        bottomMargin=48,
        title="AI RESUME ANALYZER — Compatibility Report",
        author="AI RESUME ANALYZER",
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=25,
        alignment=TA_LEFT,
        textColor=INK,
        spaceAfter=5,
    )
    heading = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=INK,
        spaceBefore=11,
        spaceAfter=6,
        keepWithNext=True,
    )
    body = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#454754"),
        spaceAfter=4,
    )
    muted = ParagraphStyle(
        "ReportMuted",
        parent=body,
        fontSize=8,
        leading=11,
        textColor=MUTED,
    )
    score_style = ParagraphStyle(
        "HeroScore",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=27,
        textColor=VIOLET,
        alignment=1,
    )

    def paragraph(value, style=body):
        return Paragraph(escape(str(value or "")), style)

    def add_page_decorations(canvas, doc):
        canvas.saveState()
        page_width, page_height = letter
        canvas.setFillColor(INK)
        canvas.rect(0, page_height - 40, page_width, 40, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawString(48, page_height - 25, "AI RESUME ANALYZER")
        canvas.setFillColor(colors.HexColor("#B8B5FF"))
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(page_width - 48, page_height - 25, "COMPATIBILITY REPORT")
        canvas.setStrokeColor(LINE)
        canvas.line(48, 36, page_width - 48, 36)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(48, 23, "Private analysis · not an employer ATS score or hiring prediction")
        canvas.drawRightString(page_width - 48, 23, f"Page {doc.page}")
        canvas.restoreState()

    job = result.get("job", {})
    job_title = job.get("job_title") or "Not specified"
    scores = result["scores"]
    score_value = float(scores.get("overall") or 0)
    story = [
        paragraph("Resume compatibility report", title),
        paragraph(
            f"Prepared {datetime.now().strftime('%B %d, %Y')}  ·  Role: {job_title}",
            muted,
        ),
        Spacer(1, 0.12 * inch),
    ]

    score_summary = Table(
        [[
            [
                paragraph("OVERALL COMPATIBILITY", muted),
                Paragraph(f"{score_value:.0f}%", score_style),
            ],
            paragraph(
                "A weighted estimate of resume and role alignment based on skill evidence, "
                "job relevance, experience, completeness, and readability.",
                body,
            ),
        ]],
        colWidths=[1.8 * inch, 4.65 * inch],
    )
    score_summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LAVENDER),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#DEDcff")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.extend([score_summary, Spacer(1, 0.08 * inch)])

    candidate = result.get("candidate", {})
    story.append(Paragraph("Candidate information", heading))
    candidate_rows = [
        [paragraph("Name", muted), paragraph(candidate.get("name") or "Not detected")],
        [paragraph("Email", muted), paragraph(candidate.get("email") or "Not detected")],
        [paragraph("Phone", muted), paragraph(candidate.get("phone") or "Not detected")],
        [paragraph("LinkedIn", muted), paragraph(candidate.get("linkedin") or "Not detected")],
        [paragraph("GitHub", muted), paragraph(candidate.get("github") or "Not detected")],
        [paragraph("Portfolio", muted), paragraph(candidate.get("portfolio") or "Not detected")],
    ]
    candidate_table = Table(candidate_rows, colWidths=[1.35 * inch, 5.1 * inch])
    candidate_table.setStyle(
        TableStyle(
            [
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, PALE]),
                ("LINEBELOW", (0, 0), (-1, -1), 0.25, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(candidate_table)

    story.append(Paragraph("Score breakdown", heading))
    score_rows = [
        [paragraph("Component", muted), paragraph("Score", muted)],
        ["Skill match", f"{float(scores.get('skill_match') or 0):.0f}%"],
        ["Job description relevance", f"{float(scores.get('text_relevance') or 0):.0f}%"],
        ["Experience relevance", f"{float(scores.get('experience_relevance') or 0):.0f}%"],
        ["Resume completeness", f"{float(scores.get('completeness') or 0):.0f}%"],
        ["Readability", f"{float(scores.get('readability') or 0):.0f}%"],
    ]
    score_table = Table(score_rows, colWidths=[4.65 * inch, 1.8 * inch])
    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), INK),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
                ("GRID", (0, 0), (-1, -1), 0.25, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TEXTCOLOR", (1, 1), (1, -1), VIOLET),
                ("FONTNAME", (1, 1), (1, -1), "Helvetica-Bold"),
            ]
        )
    )
    story.append(score_table)

    skill_match = result["skill_match"]
    story.append(Paragraph("Skills comparison", heading))
    skill_rows = [
        [
            paragraph("Requirement", muted),
            paragraph("Matched", muted),
            paragraph("Missing", muted),
        ],
        [
            "Mandatory",
            paragraph(", ".join(skill_match["required_matches"]) or "None detected"),
            paragraph(", ".join(skill_match["required_missing"]) or "None detected"),
        ],
        [
            "Preferred",
            paragraph(", ".join(skill_match["preferred_matches"]) or "None detected"),
            paragraph(", ".join(skill_match["preferred_missing"]) or "None detected"),
        ],
    ]
    skill_table = Table(
        skill_rows,
        colWidths=[1.0 * inch, 2.75 * inch, 2.7 * inch],
        repeatRows=1,
    )
    skill_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LAVENDER),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
                ("GRID", (0, 0), (-1, -1), 0.25, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(skill_table)

    ats = result.get("ats_analysis")
    if ats:
        story.append(Paragraph("Keyword analysis", heading))
        story.append(paragraph(f"Keyword coverage: {ats.get('score', 0)}%"))
        story.append(
            paragraph(
                "Found in resume: "
                + (", ".join(ats.get("matched", [])[:30]) or "None detected")
            )
        )
        story.append(
            paragraph(
                "Not found: "
                + (", ".join(ats.get("missing", [])[:30]) or "None detected")
            )
        )

    skill_gaps = result.get("skill_gaps", [])
    if skill_gaps:
        story.append(Paragraph("Prioritized skill gaps", heading))
        gap_rows = [
            [
                paragraph("Skill", muted),
                paragraph("Priority", muted),
                paragraph("Why it matters", muted),
            ]
        ]
        gap_rows.extend(
            [
                paragraph(gap.get("skill")),
                paragraph(gap.get("importance")),
                paragraph(gap.get("why")),
            ]
            for gap in skill_gaps[:12]
        )
        gap_table = Table(
            gap_rows,
            colWidths=[1.25 * inch, 1.1 * inch, 4.1 * inch],
            repeatRows=1,
        )
        gap_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), LAVENDER),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
                    ("GRID", (0, 0), (-1, -1), 0.25, LINE),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(gap_table)

    section_suggestions = result.get("section_suggestions", {})
    if section_suggestions:
        story.append(Paragraph("Resume improvement suggestions", heading))
        for section, suggestions in section_suggestions.items():
            story.append(paragraph(section))
            for suggestion in suggestions:
                story.append(paragraph("• " + suggestion, muted))

    role_recommendations = result.get("role_recommendations", [])
    if role_recommendations:
        story.append(Paragraph("Job role recommendations", heading))
        for role in role_recommendations:
            story.append(
                paragraph(
                    f"{role['role']} — {role['coverage']}% demonstrated overlap"
                )
            )

    story.append(Paragraph("Resume quality and observations", heading))
    sections = result.get("sections", {})
    story.append(
        paragraph(
            "Resume sections: "
            + (", ".join(sorted(sections.keys())) or "No standard headings detected"),
            muted,
        )
    )
    story.append(
        paragraph(
            "Readability observations: "
            + (
                "; ".join(result.get("formatting_issues", []))
                or "No major issues detected"
            ),
            muted,
        )
    )

    recommendations = result.get("recommendations", [])
    if recommendations:
        story.append(Paragraph("Recommendations", heading))
        for recommendation in recommendations:
            story.append(paragraph("• " + recommendation))

    story.append(Spacer(1, 0.1 * inch))
    story.append(
        paragraph(
            "This report provides resume-to-role guidance. It is not an employer ATS result "
            "and does not predict hiring or interview outcomes.",
            muted,
        )
    )
    document.build(
        story,
        onFirstPage=add_page_decorations,
        onLaterPages=add_page_decorations,
    )
    return output_path
