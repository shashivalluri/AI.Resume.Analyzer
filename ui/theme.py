from pathlib import Path
from html import escape

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent


def load_theme() -> None:
    css_path = BASE_DIR / "assets" / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def logo() -> str:
    return (
        "<div class='brand-lockup' aria-label='AI RESUME ANALYZER'>"
        "<div class='brand-mark'><svg viewBox='0 0 32 32' role='img' aria-hidden='true'>"
        "<path d='M16 3.5 18.8 13l9.7 3-9.7 2.8-2.8 9.7-3-9.7-9.5-2.8 9.5-3L16 3.5Z' "
        "fill='none' stroke='currentColor' stroke-width='2.1' stroke-linejoin='round'/>"
        "<circle cx='24.7' cy='7.2' r='1.5' fill='currentColor'/></svg></div>"
        "<div><div class='brand-name'>AI RESUME</div>"
        "<div class='brand-subtitle'>ANALYZER</div></div></div>"
    )


def render_metric(label: str, value: str, detail: str = "") -> str:
    return (
        f"<div class='metric-card'><div class='label'>{escape(label)}</div>"
        f"<div class='value'>{escape(value)}</div>"
        f"<div class='detail'>{escape(detail)}</div></div>"
    )


def progress_bar(value: float, color: str = "#4f46e5") -> str:
    value = max(0.0, min(100.0, float(value)))
    return f"<div class='progress'><span style='width:{value:.1f}%;background:{color}'></span></div>"
