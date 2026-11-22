from typing import Optional
import requests
import streamlit as st
from frontend.services import api_client
from frontend.components.dashboard import display_results_dashboard


def _read_jd(jd_file, jd_text: str) -> str:
    if jd_text:
        return jd_text.strip()
    if jd_file is None:
        return ""
    if jd_file.name.lower().endswith(".txt"):
        return jd_file.getvalue().decode("utf-8", errors="ignore")
    st.warning("Job description files must be `.txt` — paste the JD text instead.")
    return ""


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


def _summary_text(analysis: dict) -> str:
    score = analysis.get("ATS_score", analysis.get("ats_score", 0))
    lines = [f"ATS Score: {score:.0f}/100", ""]
    if analysis.get("strengths"):
        lines.append("STRENGTHS:")
        lines.extend(f"  - {s}" for s in analysis["strengths"])
        lines.append("")
    if analysis.get("critical_issues"):
        lines.append("CRITICAL ISSUES:")
        lines.extend(f"  - {s}" for s in analysis["critical_issues"])
        lines.append("")
    if analysis.get("suggestions"):
        lines.append("SUGGESTIONS:")
        lines.extend(f"  - {s}" for s in analysis["suggestions"])
    return "\n".join(lines)


def render(default_mode: str = "General ATS Score") -> None:
    # Page header
    st.markdown("""
    <div class="page-header">
      <div class="page-header-icon">✨</div>
      <div>
        <div class="page-header-title">AI Resume Analyzer</div>
        <div class="page-header-sub">
          Evaluate your resume, get an ATS score, and receive actionable insights.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Upload + Target job ─────────────────────────────────
    upload_col, right_col = st.columns([3, 2], gap="large")

    with upload_col:
        st.markdown("""
        <div class="upload-area">
          <div class="upload-icon">📄</div>
          <div class="upload-title">Upload Your Resume</div>
          <div class="upload-hint">Drag &amp; drop your PDF/DOCX or click to browse</div>
        </div>
        """, unsafe_allow_html=True)
        resume_file = st.file_uploader(
            "Choose your resume file",
            type=["pdf", "doc", "docx"],
            help="Supported: PDF, DOC, DOCX (max 5 MB)",
            key="resume_upload",
            label_visibility="collapsed",
        )
        if resume_file:
            st.success(f"✅ {resume_file.name}  ({resume_file.size / 1024:.1f} KB)")

    with right_col:
        # Analysis mode
        analysis_mode = st.radio(
            "Analysis mode",
            ["General ATS Score", "Job Description Comparison"],
            horizontal=False,
            index=0 if default_mode == "General ATS Score" else 1,
            key="analysis_mode_radio",
            label_visibility="collapsed",
        )

        # Target job input
        st.markdown("""
        <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:6px">
          💼 Target Job (Optional)
        </div>
        """, unsafe_allow_html=True)
        target_job = st.text_input(
            "Target Job",
            placeholder="e.g., Machine Learning Engineer",
            key="target_job",
            label_visibility="collapsed",
        )

        # JD input if needed
        jd_file: Optional[object] = None
        jd_text = ""
        if analysis_mode == "Job Description Comparison":
            st.markdown("""
            <div style="font-size:13px;font-weight:600;color:var(--text-2);
                 margin-top:12px;margin-bottom:6px">
              📋 Job Description
            </div>
            """, unsafe_allow_html=True)
            jd_method = st.radio(
                "JD input method",
                ["Paste Text", "Upload .txt File"],
                horizontal=True,
                key="jd_input_method",
                label_visibility="collapsed",
            )
            if jd_method == "Upload .txt File":
                jd_file = st.file_uploader(
                    "Choose JD file (.txt only)",
                    type=["txt"],
                    key="jd_upload",
                )
                if jd_file:
                    st.success(f"✅ {jd_file.name}")
            else:
                jd_text = st.text_area(
                    "Paste job description text:",
                    height=130,
                    placeholder="Paste the JD here...",
                    key="jd_text",
                    label_visibility="collapsed",
                )
                if jd_text:
                    st.caption(f"✅ {len(jd_text)} characters")

        # Analyze button
        st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)
        analyze = st.button(
            "Analyze Resume ✨",
            use_container_width=True,
            type="primary",
            key="analyze_btn",
            disabled=resume_file is None,
        )

    st.markdown("---")

    # ── Auth gate ───────────────────────────────────────────
    if not st.session_state.get("access_token"):
        if resume_file:
            st.markdown("""
            <div class="dark-card" style="text-align:center;padding:32px">
              <div style="font-size:28px;margin-bottom:12px">🔐</div>
              <h3 style="color:var(--text-1)">Sign in to Analyze</h3>
              <p style="color:var(--text-3)">Please sign in from the sidebar to analyze your resume.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Intro when nothing uploaded
            _show_intro()
        return

    if not resume_file:
        # Re-show previous result if available
        if st.session_state.get("scorer_analysis"):
            display_results_dashboard(st.session_state["scorer_analysis"])
            _render_export_buttons(st.session_state["scorer_analysis"])
        else:
            _show_intro()
        return

    if not analyze:
        if st.session_state.get("scorer_analysis"):
            display_results_dashboard(st.session_state["scorer_analysis"])
            _render_export_buttons(st.session_state["scorer_analysis"])
        return

    # ── Run analysis ─────────────────────────────────────────
    st.session_state.pop("scorer_pdf_bytes", None)
    st.session_state.pop("scorer_analysis", None)

    job_description = (
        _read_jd(jd_file, jd_text) if analysis_mode == "Job Description Comparison" else ""
    )

    try:
        with st.spinner("🔍 Analyzing your resume… this can take 15–30 seconds."):
            analysis = api_client.analyze_resume(
                resume_file=resume_file,
                access_token=st.session_state["access_token"],
                job_description=job_description,
            )
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    st.session_state["scorer_analysis"] = analysis
    if analysis_mode == "Job Description Comparison":
        st.session_state["job_match_analysis"] = analysis
    st.success("✅ Analysis complete!")
    display_results_dashboard(analysis)
    _render_export_buttons(analysis)


def _render_export_buttons(analysis: dict) -> None:
    import datetime
    st.markdown("---")
    st.markdown("#### 📥 Export & Save")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📑 Generate PDF Report", use_container_width=True, type="primary"):
            try:
                with st.spinner("Generating PDF…"):
                    pdf_bytes = api_client.generate_pdf(
                        analysis,
                        access_token=st.session_state["access_token"],
                    )
                st.session_state["scorer_pdf_bytes"] = pdf_bytes
            except requests.RequestException as exc:
                _show_backend_error(exc)
        if "scorer_pdf_bytes" in st.session_state:
            st.download_button(
                "⬇️ Download PDF",
                data=st.session_state["scorer_pdf_bytes"],
                file_name="ats_resume_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_pdf_report",
            )
    with c2:
        st.download_button(
            "📄 Download Summary (.txt)",
            data=_summary_text(analysis),
            file_name="ats_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_summary",
        )
    with c3:
        saved_key = f"saved_{id(analysis)}"
        already_saved = st.session_state.get(saved_key, False)
        if already_saved:
            st.markdown("""
            <div style="text-align:center;padding:10px;color:#10B981;font-size:13px;font-weight:600">
              ✅ Saved to Reports
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button("💾 Save Report", use_container_width=True):
                score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
                report_entry = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "score": score,
                    "analysis": analysis,
                    "has_jd": bool(analysis.get("jd_comparison") or analysis.get("jd_match_analysis")),
                }
                if "saved_reports_list" not in st.session_state:
                    st.session_state["saved_reports_list"] = []
                st.session_state["saved_reports_list"].insert(0, report_entry)
                st.session_state[saved_key] = True
                st.rerun()


def _show_intro() -> None:
    """Display intro cards when no resume is uploaded."""
    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:8px">
      <div class="feature-card fade-up">
        <div class="feature-icon">📊</div>
        <div class="feature-title">ATS Score</div>
        <div class="feature-desc">Get a 0–100 ATS score with breakdown across 5 key dimensions: formatting, keywords, content, skills, and compatibility.</div>
      </div>
      <div class="feature-card fade-up" style="animation-delay:.08s">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Keyword Analysis</div>
        <div class="feature-desc">See exactly which keywords your resume has and which ones are missing for your target role.</div>
      </div>
      <div class="feature-card fade-up" style="animation-delay:.16s">
        <div class="feature-icon">💡</div>
        <div class="feature-title">Actionable Tips</div>
        <div class="feature-desc">Get specific, prioritized recommendations to improve your resume and land more interviews.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
