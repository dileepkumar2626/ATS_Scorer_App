import requests
import streamlit as st
from frontend.services import api_client


def _show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the backend. Is it running on port 8000?")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        st.error(f"Backend returned {exc.response.status_code}: {exc.response.text}")
    else:
        st.error(f"Unexpected error: {exc}")


def _score_color(score: float) -> str:
    if score >= 80:
        return "#34D399"
    if score >= 60:
        return "#FBBF24"
    return "#F87171"


def render() -> None:
    st.markdown("""
    <div class="page-header">
      <div class="page-header-icon">🕐</div>
      <div>
        <div class="page-header-title">Analysis History</div>
        <div class="page-header-sub">Your past resume analyses — track your progress over time.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.markdown("""
        <div class="dark-card" style="text-align:center;padding:40px">
          <div style="font-size:36px;margin-bottom:12px">🔐</div>
          <h3 style="color:var(--text-1)">Sign in to View History</h3>
          <p style="color:var(--text-3)">Please sign in from the sidebar to view your past analyses.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    try:
        history = api_client.get_history(access_token)
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    if not history:
        st.markdown("""
        <div class="dark-card" style="text-align:center;padding:48px 32px">
          <div style="font-size:40px;margin-bottom:16px;opacity:.4">📂</div>
          <h3 style="color:var(--text-2)">No Analyses Yet</h3>
          <p style="color:var(--text-4)">Run your first resume analysis to see results here.</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎯 Analyze a Resume", use_container_width=True, type="primary"):
                st.session_state.current_view = "scorer"
                st.rerun()
        return

    st.markdown(
        f'<div style="font-size:13px;color:var(--text-3);margin-bottom:16px">'
        f'{len(history)} analyses total</div>',
        unsafe_allow_html=True,
    )

    for idx, entry in enumerate(history):
        filename   = entry.get("filename", "resume")
        ats_score  = float(entry.get("ats_score", 0))
        created_at = entry.get("created_at", "")
        analysis   = entry.get("analysis_result", {}) or {}
        cs         = analysis.get("component_scores", {}) or {}
        jd         = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")

        color = _score_color(ats_score)
        date_str = created_at[:10] if len(created_at) >= 10 else created_at

        with st.expander(f"📄 {filename}  •  Score: {ats_score:.0f}/100  •  {date_str}"):
            # Score row
            c1, c2, c3 = st.columns(3)
            c1.metric("Overall ATS",       f"{ats_score:.0f}/100")
            c2.metric("Formatting",         f"{cs.get('formatting', 0):.0f}/20")
            c3.metric("Keywords",           f"{cs.get('keywords', 0):.0f}/25")

            c4, c5, c6 = st.columns(3)
            c4.metric("Content Quality",    f"{cs.get('content', 0):.0f}/25")
            c5.metric("Skill Validation",   f"{cs.get('skill_validation', 0):.0f}/15")
            c6.metric("ATS Compatibility",  f"{cs.get('ats_compatibility', 0):.0f}/15")

            if jd:
                match = jd.get("match_percentage", 0)
                st.markdown(
                    f'<div style="font-size:13px;color:var(--text-3);margin-top:8px">'
                    f'JD Match: <strong style="color:{_score_color(match)}">{match:.0f}%</strong>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # Delete button
            entry_id = entry.get("id")
            if entry_id:
                if st.button("🗑️ Delete this entry", key=f"del_{idx}"):
                    try:
                        api_client.delete_history_entry(str(entry_id), access_token)
                        st.success("Deleted.")
                        st.rerun()
                    except requests.RequestException as exc:
                        _show_backend_error(exc)
