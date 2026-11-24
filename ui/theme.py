from pathlib import Path
from html import escape
import base64

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent


def load_theme() -> None:
    css_path = BASE_DIR / "assets" / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def logo() -> str:
    logo_path = BASE_DIR / "assets" / "logo.png"
    logo_image = ""
    if logo_path.exists():
        encoded_logo = base64.b64encode(logo_path.read_bytes()).decode("ascii")
        logo_image = (
            f"<img src='data:image/png;base64,{encoded_logo}' "
            "alt='' aria-hidden='true'/>"
        )
    return (
        "<div class='brand-lockup' aria-label='AI RESUME ANALYZER'>"
        f"<div class='brand-mark'>{logo_image or '<span style=\"font-size:16px;font-weight:700;\">✦</span>'}</div>"
        "<div><div class='brand-name'>AI RESUME</div>"
        "<div class='brand-subtitle'>ANALYZER</div></div></div>"
    )


def render_metric(label: str, value: str, detail: str = "") -> str:
    return (
        f"<div class='metric-card'><div class='label'>{escape(label)}</div>"
        f"<div class='value'>{escape(value)}</div>"
        f"<div class='detail'>{escape(detail)}</div></div>"
    )


def progress_bar(value: float, color: str = "#222222") -> str:
    value = max(0.0, min(100.0, float(value)))
    return f"<div class='progress'><span style='width:{value:.1f}%;background:{color}'></span></div>"
