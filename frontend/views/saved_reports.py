import streamlit as st
from frontend.components.dashboard import display_results_dashboard


def render() -> None:
    st.markdown("""
    <div class="page-header">
      <div class="page-header-icon">🔖</div>
      <div>
        <div class="page-header-title">Saved Reports</div>
        <div class="page-header-sub">Your saved analysis reports, most recent first.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    reports = st.session_state.get("saved_reports_list") or []

    if not reports:
        st.markdown("""
        <div class="dark-card" style="text-align:center;padding:52px 32px">
          <div style="font-size:40px;margin-bottom:16px;opacity:.4">🔖</div>
          <h3 style="color:var(--text-2)">No Saved Reports</h3>
          <p style="color:var(--text-4);max-width:420px;margin:0 auto">
            After analyzing a resume, click <strong>💾 Save Report</strong> to keep it here
            for future reference.
          </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎯 Analyze a Resume", use_container_width=True, type="primary"):
                st.session_state.current_view = "scorer"
                st.rerun()
        return

    # Summary row
    st.markdown(f"""
    <div style="font-size:13px;color:var(--text-3);margin-bottom:16px">
      {len(reports)} saved report{'s' if len(reports) != 1 else ''} ·
      Scores range from {min(r['score'] for r in reports):.0f} to {max(r['score'] for r in reports):.0f}
    </div>
    """, unsafe_allow_html=True)

    for i, report in enumerate(reports):
        score = report["score"]
        ts    = report["timestamp"]
        has_jd = report.get("has_jd", False)
        s_color = "#10B981" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
        grade   = "Great Match" if score >= 80 else "Good Match" if score >= 60 else "Needs Work"

        with st.expander(
            f"{'🟢' if score>=80 else '🟡' if score>=60 else '🔴'}  Score: {score:.0f}/100  ·  {grade}  ·  {ts}  {'· 🎯 With JD' if has_jd else ''}",
            expanded=(i == 0),
        ):
            col_del, col_load = st.columns([1, 2])
            with col_load:
                if st.button("📂 Load This Analysis", key=f"load_report_{i}", use_container_width=True, type="primary"):
                    st.session_state["scorer_analysis"] = report["analysis"]
                    if has_jd:
                        st.session_state["job_match_analysis"] = report["analysis"]
                    st.session_state.current_view = "scorer"
                    st.rerun()
            with col_del:
                if st.button("🗑️ Delete", key=f"del_report_{i}", use_container_width=True):
                    st.session_state["saved_reports_list"].pop(i)
                    st.rerun()

            st.markdown("")
            display_results_dashboard(report["analysis"])
