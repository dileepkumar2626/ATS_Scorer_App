from typing import Any, Dict, List, Tuple
import streamlit as st

SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}
SEVERITY_CLS  = {"critical": "reco-critical", "high": "reco-high",
                  "medium": "reco-medium", "low": "reco-low"}
SEVERITY_DOT  = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}


def _collect_action_items(analysis: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    items: List[Tuple[str, str, str]] = []
    for issue in analysis.get("detailed_feedback") or []:
        level = (issue.get("severity_level") or "low").lower()
        title = issue.get("issue_title", "")
        for action in issue.get("action_items") or []:
            items.append((level, title, action))
    if not items:
        for suggestion in analysis.get("suggestions") or []:
            items.append(("medium", "General", suggestion))
    items.sort(key=lambda row: SEVERITY_RANK.get(row[0], 99))
    return items


def display_action_items(analysis: Dict[str, Any]) -> None:
    items = _collect_action_items(analysis)
    if not items:
        return

    rows_html = ""
    for level, source, action in items:
        dot  = SEVERITY_DOT.get(level, "🟢")
        cls  = SEVERITY_CLS.get(level, "reco-low")
        rows_html += f"""
        <div class="reco-item">
          <div class="reco-dot {cls}">{dot}</div>
          <div>
            <span style="font-size:11px;color:var(--text-4);font-weight:600;
                  text-transform:uppercase;letter-spacing:.04em">{source}</span>
            <div style="margin-top:2px">{action}</div>
          </div>
        </div>"""

    st.markdown(f"""
    <div class="dark-card">
      <div style="font-size:15px;font-weight:600;color:var(--text-1);margin-bottom:14px">
        ⚡ Action Items
        <span style="font-size:12px;font-weight:400;color:var(--text-4);margin-left:8px">
          Sorted by urgency
        </span>
      </div>
      {rows_html}
    </div>
    """, unsafe_allow_html=True)
