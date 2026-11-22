from typing import Any, Dict, List
import streamlit as st
from frontend.components._helpers import get_severity_style

SEVERITY_ORDER = ["critical", "high", "medium", "low"]
SEVERITY_LABEL_COLOR = {
    "critical": "#F87171",
    "high":     "#FBBF24",
    "medium":   "#60A5FA",
    "low":      "#34D399",
}


def _group_by_severity(issues: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {level: [] for level in SEVERITY_ORDER}
    for issue in issues:
        level = (issue.get("severity_level") or "low").lower()
        grouped.setdefault(level, []).append(issue)
    return grouped


def _render_issue(issue: Dict[str, Any]) -> None:
    icon, text_color, bg_color = get_severity_style(issue.get("severity_level"))
    title      = issue.get("issue_title", "Untitled issue")
    impact     = issue.get("ats_impact", "")
    explanation = issue.get("explanation", "")
    where      = issue.get("where_it_appears", "")
    how_to_fix = issue.get("how_to_fix", "")
    action_items = issue.get("action_items") or []
    example    = issue.get("example_improvement", "")

    st.markdown(f"""
    <div style="border-left:3px solid {text_color};background:rgba(0,0,0,.2);
         padding:10px 14px;border-radius:0 var(--radius-md) var(--radius-md) 0;
         margin-bottom:8px">
      <div style="font-weight:600;color:{text_color};font-size:14px">
        {icon} {title}
      </div>
      {f'<div style="font-size:12px;color:var(--text-4);margin-top:2px">{impact}</div>' if impact else ''}
    </div>
    """, unsafe_allow_html=True)

    with st.expander("View details", expanded=False):
        if explanation:
            st.markdown(f"**What's happening:** {explanation}")
        if where:
            st.markdown(f"**Where:** {where}")
        if how_to_fix:
            st.markdown(f"**How to fix:** {how_to_fix}")
        if action_items:
            st.markdown("**Action items:**")
            for item in action_items:
                st.markdown(f"- {item}")
        if example:
            st.markdown("**Example improvement:**")
            st.code(example, language="text")


def display_detailed_feedback(analysis: Dict[str, Any]) -> None:
    issues = analysis.get("detailed_feedback") or []
    if not issues:
        return

    grouped = _group_by_severity(issues)

    st.markdown(f"""
    <div style="font-size:15px;font-weight:600;color:var(--text-1);margin-bottom:14px">
      🔍 Detailed Feedback
      <span style="font-size:12px;font-weight:400;color:var(--text-4);margin-left:8px">
        {len(issues)} issue(s) flagged
      </span>
    </div>
    """, unsafe_allow_html=True)

    for level in SEVERITY_ORDER:
        items = grouped.get(level, [])
        if not items:
            continue
        label_color = SEVERITY_LABEL_COLOR.get(level, "#8B949E")
        st.markdown(
            f'<div style="font-size:12px;font-weight:600;color:{label_color};'
            f'text-transform:uppercase;letter-spacing:.06em;margin:14px 0 6px">'
            f'{level.title()} ({len(items)})</div>',
            unsafe_allow_html=True,
        )
        for issue in items:
            _render_issue(issue)
