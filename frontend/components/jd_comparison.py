from typing import Any, Dict, Optional
import streamlit as st


def display_jd_comparison(jd_comparison: Optional[Dict[str, Any]]) -> None:
    if not jd_comparison:
        return

    match_pct  = float(jd_comparison.get("match_percentage",   0))
    semantic   = float(jd_comparison.get("semantic_similarity", 0))
    matched    = jd_comparison.get("matched_keywords", []) or []
    missing    = jd_comparison.get("missing_keywords",  []) or []
    gap        = jd_comparison.get("skills_gap",         []) or []

    # Header metrics
    m1, m2 = st.columns(2)
    pct_color = "#10B981" if match_pct >= 80 else "#F59E0B" if match_pct >= 60 else "#EF4444"
    m1.metric("Match Percentage",   f"{match_pct:.0f}%")
    m2.metric("Semantic Similarity", f"{semantic * 100:.0f}%")

    pct_cls = "prog-green" if match_pct >= 80 else "prog-yellow" if match_pct >= 60 else "prog-red"
    st.markdown(f"""
    <div class="prog-wrap">
      <div class="prog-label">
        <span>JD Match</span>
        <span style="color:{pct_color};font-weight:700">{match_pct:.0f}%</span>
      </div>
      <div class="prog-track">
        <div class="prog-fill {pct_cls}" style="width:{match_pct:.1f}%"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Matched keywords
    if matched:
        tags = "".join(f'<span class="kw-tag kw-matched">✓ {k}</span>' for k in matched[:20])
        st.markdown(f"""
        <div class="dark-card-sm" style="margin-top:14px">
          <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:10px">
            ✅ Matched Keywords ({len(matched)})
          </div>
          <div class="keyword-tags">{tags}</div>
        </div>
        """, unsafe_allow_html=True)

    # Missing keywords + skills gap
    left, right = st.columns(2)
    with left:
        if missing:
            tags = "".join(f'<span class="kw-tag kw-missing">✗ {k}</span>' for k in missing[:15])
            st.markdown(f"""
            <div class="dark-card-sm" style="margin-top:14px">
              <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:10px">
                ❌ Missing Keywords ({len(missing)})
              </div>
              <div class="keyword-tags">{tags}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="dark-card-sm" style="margin-top:14px;text-align:center">
              <span style="color:var(--green2)">✅ All key terms are present!</span>
            </div>
            """, unsafe_allow_html=True)

    with right:
        if gap:
            rows = "".join(
                f'<div class="skill-row"><span>{s}</span>'
                f'<span class="priority-{"high" if i < 2 else "medium"}">'
                f'{"High" if i < 2 else "Medium"}</span></div>'
                for i, s in enumerate(gap[:8])
            )
            st.markdown(f"""
            <div class="dark-card-sm" style="margin-top:14px">
              <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:10px">
                📊 Skills Gap ({len(gap)})
              </div>
              {rows}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="dark-card-sm" style="margin-top:14px;text-align:center">
              <span style="color:var(--green2)">✅ No significant skills gap detected!</span>
            </div>
            """, unsafe_allow_html=True)
