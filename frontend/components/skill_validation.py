from typing import Any, Dict
import streamlit as st


def display_skill_validation(analysis: Dict[str, Any]) -> None:
    details = analysis.get("skill_validation_details") or {}
    validated   = details.get("validated", [])
    unvalidated = details.get("unvalidated", [])
    total       = details.get("total", len(validated) + len(unvalidated))
    pct         = details.get("validation_pct", 0.0)

    if total == 0:
        st.info("No skills detected on the resume.")
        return

    # Stats row
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Skills",   total)
    c2.metric("Validated",      len(validated))
    c3.metric("Validation %",   f"{pct:.0f}%")

    pct_cls = "prog-green" if pct >= 80 else "prog-yellow" if pct >= 60 else "prog-red"
    st.markdown(f"""
    <div class="prog-wrap" style="margin-bottom:16px">
      <div class="prog-track">
        <div class="prog-fill {pct_cls}" style="width:{pct:.1f}%"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Validated skills
    if validated:
        tags = "".join(
            f'<span class="kw-tag kw-matched">✓ {e.get("skill","?")}</span>'
            for e in validated
        )
        st.markdown(f"""
        <div class="dark-card-sm" style="margin-bottom:12px">
          <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:10px">
            ✅ Validated Skills ({len(validated)})
          </div>
          <div class="keyword-tags">{tags}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("See validation details"):
            for entry in validated:
                skill    = entry.get("skill", "?")
                projects = entry.get("projects", []) or []
                sim      = entry.get("similarity")
                proj_txt = ", ".join(projects[:3]) if projects else "experience section"
                sim_txt  = f" ({sim * 100:.0f}% match)" if isinstance(sim, (int, float)) else ""
                st.markdown(f"- **{skill}**{sim_txt} — in: {proj_txt}")

    # Unvalidated skills
    if unvalidated:
        tags = "".join(
            f'<span class="kw-tag kw-missing">! {s}</span>'
            for s in unvalidated
        )
        st.markdown(f"""
        <div class="dark-card-sm">
          <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:6px">
            ⚠️ Unvalidated Skills ({len(unvalidated)})
          </div>
          <div style="font-size:12px;color:var(--text-4);margin-bottom:10px">
            Listed but not tied to a project or experience bullet.
          </div>
          <div class="keyword-tags">{tags}</div>
        </div>
        """, unsafe_allow_html=True)
