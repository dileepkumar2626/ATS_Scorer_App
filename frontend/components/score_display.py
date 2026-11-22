from typing import Any, Dict
import streamlit as st
from frontend.components._helpers import get_score_color, get_score_emoji

COMPONENTS = [
    ("Formatting",        "formatting",        20, "📝"),
    ("Keywords & Skills", "keywords",          25, "🔑"),
    ("Content Quality",   "content",           25, "📄"),
    ("Skill Validation",  "skill_validation",  15, "✅"),
    ("ATS Compatibility", "ats_compatibility", 15, "🤖"),
]


def _score_svg(score: float, label: str = "ATS Score", size: int = 190) -> str:
    r = 72
    circ = 2 * 3.14159265 * r
    offset = circ * (1.0 - min(max(score, 0), 100) / 100.0)

    if score >= 80:
        c1, c2 = "#10B981", "#34D399"
    elif score >= 60:
        c1, c2 = "#F59E0B", "#FBBF24"
    else:
        c1, c2 = "#EF4444", "#F87171"

    return f"""
    <svg viewBox="0 0 200 200" width="{size}" height="{size}">
      <defs>
        <linearGradient id="sg_{int(score)}" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%"   style="stop-color:{c1};stop-opacity:1"/>
          <stop offset="100%" style="stop-color:{c2};stop-opacity:1"/>
        </linearGradient>
      </defs>
      <circle cx="100" cy="100" r="{r}"
        fill="none" stroke="#2D3448" stroke-width="14"/>
      <circle cx="100" cy="100" r="{r}"
        fill="none"
        stroke="url(#sg_{int(score)})" stroke-width="14"
        stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}"
        stroke-linecap="round"
        transform="rotate(-90,100,100)"/>
      <text x="100" y="92" text-anchor="middle"
        fill="#F0F6FC" font-size="34" font-weight="700"
        font-family="-apple-system,BlinkMacSystemFont,sans-serif">{score:.0f}%</text>
      <text x="100" y="114" text-anchor="middle"
        fill="#8B949E" font-size="13"
        font-family="-apple-system,BlinkMacSystemFont,sans-serif">{label}</text>
    </svg>
    """


def _prog_bar(value: float, max_val: float, label: str, icon: str) -> str:
    pct = min(max(value / max_val if max_val else 0, 0), 1) * 100
    if pct >= 80:
        cls = "prog-green"
    elif pct >= 60:
        cls = "prog-yellow"
    else:
        cls = "prog-red"
    # Single-line HTML — no newlines/blank-lines so Python-Markdown's HTML block
    # parser never exits HTML mode mid-string and renders subsequent bars as code.
    return (
        f'<div class="prog-wrap">'
        f'<div class="prog-label">'
        f'<span>{icon} {label}</span>'
        f'<span style="font-weight:600;color:#F0F6FC">{value:.0f}/{max_val:.0f}</span>'
        f'</div>'
        f'<div class="prog-track">'
        f'<div class="prog-fill {cls}" style="width:{pct:.1f}%"></div>'
        f'</div>'
        f'</div>'
    )


def display_overall_score(analysis: Dict[str, Any]) -> None:
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    interpretation = analysis.get("interpretation", "")

    if score >= 80:
        grade = "Great Match! 🎯"
        grade_color = "#10B981"
        badge_html = """
        <div class="badge-row">
          <span class="badge badge-green">✓ ATS Friendly</span>
          <span class="badge badge-green">✓ Relevant Skills</span>
          <span class="badge badge-green">✓ Good Structure</span>
        </div>"""
    elif score >= 60:
        grade = "Good Match 👍"
        grade_color = "#F59E0B"
        badge_html = """
        <div class="badge-row">
          <span class="badge badge-green">✓ ATS Friendly</span>
          <span class="badge badge-yellow">⚡ Needs Keywords</span>
          <span class="badge badge-yellow">⚡ Improve Content</span>
        </div>"""
    else:
        grade = "Needs Improvement 📝"
        grade_color = "#EF4444"
        badge_html = """
        <div class="badge-row">
          <span class="badge badge-red">✗ ATS Issues</span>
          <span class="badge badge-red">✗ Missing Keywords</span>
          <span class="badge badge-yellow">⚡ Structure Issues</span>
        </div>"""

    left, right = st.columns([1, 2])
    with left:
        st.markdown(
            f'<div class="score-wrap">{_score_svg(score)}</div>',
            unsafe_allow_html=True,
        )
    with right:
        interp = interpretation or "Your resume has been analyzed. See the detailed breakdown below."
        st.markdown(
            f'<div style="padding:12px 0;">'
            f'<h2 style="color:{grade_color};margin:0 0 6px;font-size:26px">{grade}</h2>'
            f'<p style="color:#8B949E;margin:0 0 14px;font-size:14px;line-height:1.5">{interp}</p>'
            f'{badge_html}'
            f'</div>',
            unsafe_allow_html=True,
        )


def display_score_breakdown(analysis: Dict[str, Any]) -> None:
    component_scores = analysis.get("component_scores") or {}
    st.markdown("#### 📈 Score Breakdown")

    bars_html = "".join(
        _prog_bar(
            float(component_scores.get(key, 0)),
            float(max_score),
            label,
            icon,
        )
        for label, key, max_score, icon in COMPONENTS
    )
    st.markdown(
        f'<div class="dark-card" style="padding:16px 20px">{bars_html}</div>',
        unsafe_allow_html=True,
    )
