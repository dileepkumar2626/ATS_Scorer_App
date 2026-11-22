from typing import Any, Dict
import streamlit as st


def display_recommendations(analysis: Dict[str, Any]) -> None:
    suggestions = analysis.get("suggestions") or []
    if not suggestions:
        return

    items_html = "".join(
        f"""
        <div class="reco-item">
          <div class="reco-dot reco-medium" style="font-size:12px">✓</div>
          <span>{s}</span>
        </div>"""
        for s in suggestions
    )

    st.markdown(f"""
    <div class="dark-card">
      <div style="font-size:15px;font-weight:600;color:var(--text-1);margin-bottom:14px">
        💡 Recommendations
      </div>
      {items_html}
    </div>
    """, unsafe_allow_html=True)
