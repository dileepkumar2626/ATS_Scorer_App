from typing import Any, Dict, List
import streamlit as st


def display_strengths(strengths: List[str]) -> None:
    if not strengths:
        return
    items_html = "".join(
        f'<div class="reco-item"><div class="reco-dot reco-low" style="font-size:10px">✓</div>'
        f'<span>{item}</span></div>'
        for item in strengths
    )
    st.markdown(f"""
    <div class="dark-card-sm">
      <div style="font-size:14px;font-weight:600;color:var(--text-1);margin-bottom:10px">
        💪 Strengths
      </div>
      {items_html}
    </div>
    """, unsafe_allow_html=True)


def display_critical_issues(analysis: Dict[str, Any]) -> None:
    critical = analysis.get("critical_issues") or []
    summary  = analysis.get("issues_summary") or []

    if not critical and not summary:
        st.markdown("""
        <div class="dark-card-sm" style="border-color:rgba(16,185,129,.3)">
          <span style="color:var(--green2)">✅ No Critical Issues Found!</span>
          <div style="font-size:12px;color:var(--text-4);margin-top:4px">
            Your resume doesn't have any urgent issues. Nice work!
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    items_html = "".join(
        f'<div class="reco-item"><div class="reco-dot reco-critical" style="font-size:10px">!</div>'
        f'<span>{item}</span></div>'
        for item in critical
    )
    extra = [s for s in summary if s not in critical]
    st.markdown(f"""
    <div class="dark-card-sm" style="border-color:rgba(239,68,68,.3)">
      <div style="font-size:14px;font-weight:600;color:#F87171;margin-bottom:10px">
        🚨 Critical Issues
      </div>
      {items_html}
    </div>
    """, unsafe_allow_html=True)

    if extra:
        with st.expander("📋 Additional flagged items"):
            for item in extra:
                st.markdown(f"- {item}")
