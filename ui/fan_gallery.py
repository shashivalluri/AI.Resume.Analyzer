import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

BASE_DIR = Path(__file__).resolve().parent.parent
CARDS_DIR = BASE_DIR / "assets" / "cards"
CSS_FILE = BASE_DIR / "components" / "fan-gallery.css"
BUNDLE_FILE = BASE_DIR / "assets" / "fan-gallery.bundle.js"

DEFAULT_GALLERY_ITEMS = [
    {
        "filename": "ats-score.webp",
        "alt": "AI Resume Analyzer ATS Score & Compatibility Overview",
    },
    {
        "filename": "skill-gap.webp",
        "alt": "Skill Gap Taxonomy & Requirement Matching",
    },
    {
        "filename": "resume-preview.webp",
        "alt": "Executive Resume Structure and Section Breakdown",
    },
    {
        "filename": "improvements.webp",
        "alt": "Actionable Bullet Point Improvements and Score Boost",
    },
    {
        "filename": "job-recommendations.webp",
        "alt": "Target Role Recommendations and Alignment",
    },
]

@st.cache_data
def _load_gallery_assets() -> tuple[str, str, list[dict]]:
    css_content = CSS_FILE.read_text(encoding="utf-8") if CSS_FILE.exists() else ""
    js_content = BUNDLE_FILE.read_text(encoding="utf-8") if BUNDLE_FILE.exists() else ""

    encoded_items = []
    for item in DEFAULT_GALLERY_ITEMS:
        img_path = CARDS_DIR / item["filename"]
        if img_path.exists():
            data_b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
            data_uri = f"data:image/webp;base64,{data_b64}"
        else:
            data_uri = ""
        encoded_items.append({
            "src": data_uri,
            "alt": item["alt"]
        })

    return css_content, js_content, encoded_items


def render_fan_gallery(
    card_width: int = 162,
    aspect_ratio: float = 0.8,
    spacing: float = 0.69,
    curve: float = 0.14,
    tilt: float = 14.5,
    lift: int = 42,
    spread: float = 0.2,
    stack_from: str = "left",
    speed: float = 0.7,
    stagger: float = 0.09,
    bounce: float = 0.35,
    hover_speed: float = 0.28,
    radius: int = 18,
    entrance: str = "stack",
    trigger: str = "scroll",
    viewport_start: int = 75,
    once: bool = True,
    show_title: bool = False,
    height: int = 330,
) -> None:
    """Renders the interactive ReactDrops Fan Gallery component inside Streamlit."""
    css, js, items = _load_gallery_assets()

    import json
    items_json = json.dumps(items)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
          background: transparent;
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
          overflow: hidden;
          color: #161B1D;
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 100vh;
        }}
        {css}
        .fan-gallery {{
          padding: 10px 0 0 0;
          max-width: 1000px;
          margin: 0 auto;
        }}
        .fan-gallery-card {{
          border-radius: 8px;
          border: 1px solid #D1D5DC;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), inset 0 0 0 1px rgba(2, 6, 19, 0.04);
          transition: box-shadow 0.2s ease, border-color 0.2s ease;
          background: #FFFFFF;
        }}
        .fan-gallery-card:hover, .fan-gallery-card:focus {{
          border-color: #2DC08D;
          box-shadow: 0 8px 24px -4px rgba(45, 192, 141, 0.25), 0 0 0 2px #2DC08D;
        }}
      </style>
    </head>
    <body>
      <div id="gallery-container"></div>
      <script>
        {js}
        const items = {items_json};
        const options = {{
          cardWidth: {card_width},
          aspectRatio: {aspect_ratio},
          spacing: {spacing},
          curve: {curve},
          tilt: {tilt},
          lift: {lift},
          spread: {spread},
          stackFrom: "{stack_from}",
          speed: {speed},
          stagger: {stagger},
          bounce: {bounce},
          hoverSpeed: {hover_speed},
          radius: {radius},
          entrance: "{entrance}",
          trigger: "{trigger}",
          viewportStart: {viewport_start},
          once: {str(once).lower()},
          showTitle: {str(show_title).lower()}
        }};

        const container = document.getElementById('gallery-container');
        if (window.initFanGallery) {{
          window.initFanGallery(container, items, options);
        }}
      </script>
    </body>
    </html>
    """

    components.html(html_content, height=height, scrolling=False)
