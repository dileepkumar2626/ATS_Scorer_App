from typing import Optional
import datetime
import requests
import streamlit as st
from frontend.services import api_client
from frontend.components.score_display import display_overall_score, display_score_breakdown
from frontend.components.strengths_issues import display_strengths, display_critical_issues
from frontend.components.skill_validation import display_skill_validation
from frontend.components.jd_comparison import display_jd_comparison


def _show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the backend. Is `uvicorn backend.main:app` running on port 8000?")
    elif isinstance(exc, requests.Timeout):
        st.error("The backend took too long to respond. Try a smaller resume.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        st.error(f"Backend returned {exc.response.status_code}: {detail}")
    else:
        st.error(f"Unexpected error: {exc}")


def render() -> None:
    st.markdown("""
    <div class="page-header">
      <div class="page-header-icon">💼</div>
      <div>
        <div class="page-header-title">Job Match Analysis</div>
        <div class="page-header-sub">
          Upload your resume + paste a job description to see how well you match.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Upload area ─────────────────────────────────────────
    up_col, jd_col = st.columns([1, 1], gap="large")

    with up_col:
        st.markdown("""
        <div class="upload-area">
          <div class="upload-icon">📄</div>
          <div class="upload-title">Upload Your Resume</div>
          <div class="upload-hint">PDF, DOC, or DOCX — max 5 MB</div>
        </div>
        """, unsafe_allow_html=True)
        resume_file = st.file_uploader(
            "Resume", type=["pdf", "doc", "docx"],
            key="jm_resume_upload", label_visibility="collapsed",
        )
        if resume_file:
            st.success(f"✅ {resume_file.name}  ({resume_file.size / 1024:.1f} KB)")

    with jd_col:
        st.markdown("""
        <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:8px">
          📋 Job Description
        </div>
        """, unsafe_allow_html=True)
        jd_method = st.radio(
            "JD method", ["Paste Text", "Upload .txt File"],
            horizontal=True, key="jm_jd_method", label_visibility="collapsed",
        )
        jd_text = ""
        jd_file: Optional[object] = None
        if jd_method == "Upload .txt File":
            jd_file = st.file_uploader(
                "JD file", type=["txt"], key="jm_jd_upload", label_visibility="collapsed",
            )
            if jd_file:
                st.success(f"✅ {jd_file.name}")
        else:
            jd_text = st.text_area(
                "Paste JD",
                height=180,
                placeholder="Paste the full job description here...",
                key="jm_jd_text",
                label_visibility="collapsed",
            )
            if jd_text:
                st.caption(f"✅ {len(jd_text)} characters")

        st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
        analyze = st.button(
            "Run Job Match Analysis 🔍",
            use_container_width=True,
            type="primary",
            key="jm_analyze_btn",
            disabled=(resume_file is None),
        )

    st.markdown("---")

    # ── Auth gate ───────────────────────────────────────────
    if not st.session_state.get("access_token"):
        if resume_file:
            st.markdown("""
            <div class="dark-card" style="text-align:center;padding:32px">
              <div style="font-size:28px;margin-bottom:12px">🔐</div>
              <h3 style="color:var(--text-1)">Sign in Required</h3>
              <p style="color:var(--text-3)">Please sign in from the sidebar to run the analysis.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            _show_intro()
        return

    if not resume_file:
        # Show cached result if available
        if st.session_state.get("job_match_analysis"):
            _render_results(st.session_state["job_match_analysis"])
        else:
            _show_intro()
        return

    if not analyze:
        if st.session_state.get("job_match_analysis"):
            _render_results(st.session_state["job_match_analysis"])
        return

    # ── Run analysis ─────────────────────────────────────────
    # Prepare JD string
    if jd_file:
        job_description = jd_file.getvalue().decode("utf-8", errors="ignore")
    else:
        job_description = jd_text.strip()

    if not job_description:
        st.warning("⚠️ Please provide a job description to run a match analysis.")
        return

    st.session_state.pop("job_match_analysis", None)

    try:
        with st.spinner("🔍 Analyzing your resume against the job description…"):
            analysis = api_client.analyze_resume(
                resume_file=resume_file,
                access_token=st.session_state["access_token"],
                job_description=job_description,
            )
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    # Save to both keys so Skill Gap and other pages can access it
    st.session_state["job_match_analysis"] = analysis
    st.session_state["scorer_analysis"]    = analysis

    st.success("✅ Match analysis complete!")
    _render_results(analysis)


def _render_results(analysis: dict) -> None:
    jd = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
    match_pct = float(jd.get("match_percentage", 0)) if jd else 0
    pct_color = "#10B981" if match_pct >= 80 else "#F59E0B" if match_pct >= 60 else "#EF4444"
    prog_cls  = "prog-green" if match_pct >= 80 else "prog-yellow" if match_pct >= 60 else "prog-red"

    # ── Top match score banner + save ───────────────────────
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    s_color = "#10B981" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
    saved_key = f"jm_saved_{id(analysis)}"

    banner_col, _, score_col, save_col = st.columns([3, 1, 1, 1])
    with banner_col:
        st.markdown(f"""
        <div class="dark-card" style="border-color:rgba(124,58,237,.35)">
          <div style="font-size:13px;font-weight:600;color:var(--text-3);margin-bottom:6px">
            🎯 Match with Job Description
          </div>
          <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px">
            <span style="font-size:40px;font-weight:800;color:{pct_color}">{match_pct:.0f}%</span>
            <div style="flex:1">
              <div class="prog-track" style="height:10px">
                <div class="prog-fill {prog_cls}" style="width:{match_pct:.1f}%"></div>
              </div>
              <div style="font-size:11px;color:var(--text-4);margin-top:4px">
                {'Great match! You are well-aligned with this role.' if match_pct >= 80
                 else 'Good match. Add missing keywords to improve.' if match_pct >= 60
                 else 'Low match. Tailor your resume significantly for this role.'}
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with score_col:
        st.markdown(f"""
        <div class="dark-card" style="text-align:center">
          <div style="font-size:11px;color:var(--text-4);margin-bottom:4px">ATS Score</div>
          <div style="font-size:36px;font-weight:800;color:{s_color};line-height:1">{score:.0f}</div>
          <div style="font-size:11px;color:var(--text-4)">/100</div>
        </div>
        """, unsafe_allow_html=True)
    with save_col:
        if st.session_state.get(saved_key):
            st.markdown("""
            <div class="dark-card" style="text-align:center;padding:14px 8px;
                 border-color:rgba(16,185,129,.35)">
              <div style="font-size:18px">✅</div>
              <div style="font-size:11px;color:#10B981;font-weight:600">Saved!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
            if st.button("🔖 Save Report", use_container_width=True, key=f"jm_save_btn_{id(analysis)}"):
                entry = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "score": score,
                    "analysis": analysis,
                    "has_jd": bool(jd),
                }
                if "saved_reports_list" not in st.session_state:
                    st.session_state["saved_reports_list"] = []
                st.session_state["saved_reports_list"].insert(0, entry)
                st.session_state[saved_key] = True
                st.rerun()

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────
    t1, t2, t3, t4, t5 = st.tabs([
        "🎯 JD Comparison",
        "📊 Score Breakdown",
        "💪 Strengths & Issues",
        "🎓 Skill Validation",
        "🔍 Keywords",
    ])

    with t1:
        if jd:
            display_jd_comparison(jd)
        else:
            st.info("No JD data available. Run the analysis with a job description.")

    with t2:
        display_overall_score(analysis)
        st.markdown("")
        display_score_breakdown(analysis)

    with t3:
        strengths = analysis.get("strengths") or []
        display_strengths(strengths)
        st.markdown("")
        display_critical_issues(analysis)

    with t4:
        display_skill_validation(analysis)

    with t5:
        if jd:
            matched = jd.get("matched_keywords", []) or []
            missing = jd.get("missing_keywords",  []) or []
            if matched or missing:
                m_tags = "".join(f'<span class="kw-tag kw-matched">✓ {k}</span>' for k in matched[:25])
                x_tags = "".join(f'<span class="kw-tag kw-missing">✗ {k}</span>' for k in missing[:25])
                c1, c2 = st.columns(2)
                c1.metric("Matched Keywords", len(matched))
                c2.metric("Missing Keywords", len(missing))
                st.markdown(f"""
                <div class="dark-card" style="margin-top:12px">
                  <div class="keyword-tags">{m_tags}{x_tags}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Add a job description to see keyword analysis.")

    # ── Skill gap CTA ─────────────────────────────────────────
    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 View Full Skill Gap", use_container_width=True):
            st.session_state.current_view = "skill_gap"
            st.rerun()
    with col2:
        if st.button("📝 Build a Better Resume", use_container_width=True, type="primary"):
            st.session_state.current_view = "builder"
            st.rerun()


def _show_intro() -> None:
    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">
      <div class="feature-card fade-up">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Keyword Match</div>
        <div class="feature-desc">See exactly which JD keywords your resume has and which ones are missing — with green/red tags.</div>
      </div>
      <div class="feature-card fade-up" style="animation-delay:.08s">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Score Breakdown</div>
        <div class="feature-desc">Get a full 5-dimension ATS score plus a JD match percentage with semantic similarity.</div>
      </div>
      <div class="feature-card fade-up" style="animation-delay:.16s">
        <div class="feature-icon">💪</div>
        <div class="feature-title">Strengths & Issues</div>
        <div class="feature-desc">See what's working in your resume and what critical issues to fix before applying.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
