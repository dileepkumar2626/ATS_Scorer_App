from typing import Any, Dict
import datetime
import streamlit as st

from frontend.components.score_display import display_overall_score, display_score_breakdown
from frontend.components.strengths_issues import display_strengths, display_critical_issues
from frontend.components.skill_validation import display_skill_validation
from frontend.components.jd_comparison import display_jd_comparison


def _right_panel(analysis: Dict[str, Any]) -> None:
    """Right sidebar panel: save button, job match %, missing skills, suggestions."""
    # ── Save Report button (always visible) ─────────────────
    saved_key = f"dash_saved_{id(analysis)}"
    if st.session_state.get(saved_key):
        st.markdown("""
        <div style="text-align:center;padding:8px 0;color:#10B981;font-size:12px;
             font-weight:600;border:1px solid rgba(16,185,129,.3);border-radius:8px;
             background:rgba(16,185,129,.08);margin-bottom:10px">
          ✅ Saved to Reports
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.button("💾 Save Report", use_container_width=True, key=f"save_btn_{id(analysis)}"):
            score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
            entry = {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "score": score,
                "analysis": analysis,
                "has_jd": bool(analysis.get("jd_comparison") or analysis.get("jd_match_analysis")),
            }
            if "saved_reports_list" not in st.session_state:
                st.session_state["saved_reports_list"] = []
            st.session_state["saved_reports_list"].insert(0, entry)
            st.session_state[saved_key] = True
            st.rerun()

    jd = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")

    # ── Match with Job Description ──────────────────────────
    if jd:
        match_pct = float(jd.get("match_percentage", 0))
        pct_color = "#10B981" if match_pct >= 80 else "#F59E0B" if match_pct >= 60 else "#EF4444"
        prog_cls = "prog-green" if match_pct >= 80 else "prog-yellow" if match_pct >= 60 else "prog-red"
        st.markdown(
            '<div class="dark-card-sm">'
            '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">'
            f'<span style="font-size:13px;font-weight:600;color:#C9D1D9">🎯 Match with JD</span>'
            f'<span style="font-size:18px;font-weight:700;color:{pct_color}">{match_pct:.0f}%</span>'
            '</div>'
            f'<div class="prog-track"><div class="prog-fill {prog_cls}" style="width:{match_pct:.1f}%"></div></div>'
            '</div>',
            unsafe_allow_html=True,
        )

        # Missing keywords as skills gap
        missing = jd.get("missing_keywords") or jd.get("skills_gap") or []
        if missing:
            skills_html = ""
            for i, skill in enumerate(missing[:6]):
                priority = "High" if i < 2 else "Medium" if i < 4 else "Low"
                p_cls = "priority-high" if i < 2 else "priority-medium" if i < 4 else "priority-low"
                skills_html += f'<div class="skill-row"><span>{skill}</span><span class="{p_cls}">{priority}</span></div>'
            st.markdown(
                '<div class="dark-card-sm" style="margin-top:10px">'
                '<div style="font-size:13px;font-weight:600;color:#C9D1D9;margin-bottom:10px">🧩 Top Missing Skills</div>'
                f'{skills_html}'
                '</div>',
                unsafe_allow_html=True,
            )

    # ── Actionable Suggestions ──────────────────────────────
    suggestions = analysis.get("suggestions") or []
    if suggestions:
        items_html = "".join(
            f'<div class="reco-item"><div class="reco-dot reco-medium">✓</div><span>{s}</span></div>'
            for s in suggestions[:5]
        )
        st.markdown(
            '<div class="dark-card-sm" style="margin-top:10px">'
            '<div style="font-size:13px;font-weight:600;color:#C9D1D9;margin-bottom:10px">💡 Actionable Suggestions</div>'
            f'{items_html}'
            '</div>',
            unsafe_allow_html=True,
        )

    # ── Score breakdown ─────────────────────────────────────
    component_scores = analysis.get("component_scores") or {}
    if component_scores:
        COMPS = [
            ("Formatting",   "formatting",        20),
            ("Keywords",     "keywords",          25),
            ("Content",      "content",           25),
            ("Validation",   "skill_validation",  15),
            ("ATS Compat.",  "ats_compatibility", 15),
        ]
        boxes_html = ""
        for label, key, max_v in COMPS:
            val = float(component_scores.get(key, 0))
            pct = val / max_v * 100 if max_v else 0
            color = "#10B981" if pct >= 80 else "#F59E0B" if pct >= 60 else "#EF4444"
            boxes_html += (
                f'<div style="text-align:center;padding:8px 4px">'
                f'<div style="font-size:16px;font-weight:700;color:{color}">{val:.0f}</div>'
                f'<div style="font-size:10px;color:#6E7681">{label}</div>'
                f'</div>'
            )
        st.markdown(
            '<div class="dark-card-sm" style="margin-top:10px">'
            '<div style="font-size:13px;font-weight:600;color:#C9D1D9;margin-bottom:8px">📊 Component Scores</div>'
            f'<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:4px">{boxes_html}</div>'
            '</div>',
            unsafe_allow_html=True,
        )


def _tab_skills(analysis: Dict[str, Any]) -> None:
    display_skill_validation(analysis)


def _tab_jd_comparison(analysis: Dict[str, Any]) -> None:
    jd = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
    if jd:
        display_jd_comparison(jd)
    else:
        st.markdown(
            '<div class="dark-card" style="text-align:center;padding:36px 24px">'
            '<div style="font-size:32px;margin-bottom:12px;opacity:.4">🎯</div>'
            '<h4 style="color:#C9D1D9;margin-bottom:8px">No Job Description Yet</h4>'
            '<p style="color:#6E7681;max-width:400px;margin:0 auto">Re-analyze with a job description pasted to see keyword matching, semantic similarity, and a detailed match breakdown.</p>'
            '</div>',
            unsafe_allow_html=True,
        )

        # Fallback: show resume skills as neutral tags
        details = analysis.get("skill_validation_details") or {}
        all_skills = [
            e.get("skill") for e in (details.get("validated") or []) if e.get("skill")
        ] + (details.get("unvalidated") or [])
        if all_skills:
            tags_html = "".join(
                f'<span class="kw-tag kw-matched">✓ {s}</span>' for s in all_skills[:30]
            )
            st.markdown(
                '<div class="dark-card" style="margin-top:12px">'
                '<div style="font-size:13px;font-weight:600;color:#C9D1D9;margin-bottom:10px">Your Resume Skills</div>'
                f'<div class="keyword-tags">{tags_html}</div>'
                '</div>',
                unsafe_allow_html=True,
            )


def _tab_keywords_only(analysis: Dict[str, Any]) -> None:
    jd = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
    if jd:
        matched = jd.get("matched_keywords") or []
        missing = jd.get("missing_keywords") or []
        if matched or missing:
            c1, c2 = st.columns(2)
            c1.metric("Matched Keywords", len(matched))
            c2.metric("Missing Keywords", len(missing))
            m_tags = "".join(f'<span class="kw-tag kw-matched">✓ {k}</span>' for k in matched[:25])
            x_tags = "".join(f'<span class="kw-tag kw-missing">✗ {k}</span>' for k in missing[:25])
            st.markdown(
                f'<div class="dark-card" style="margin-top:10px"><div class="keyword-tags">{m_tags}{x_tags}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.info("No keyword data found in this analysis.")
    else:
        st.markdown(
            '<div class="dark-card" style="text-align:center;padding:28px">'
            '<div style="font-size:28px;margin-bottom:8px;opacity:.4">🔍</div>'
            '<p style="color:#8B949E">Add a job description to see keyword matching.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        # Show all resume skills as neutral tags
        details = analysis.get("skill_validation_details") or {}
        all_skills = [
            e.get("skill") for e in (details.get("validated") or []) if e.get("skill")
        ] + (details.get("unvalidated") or [])
        if all_skills:
            tags_html = "".join(
                f'<span class="kw-tag kw-matched">✓ {s}</span>' for s in all_skills[:30]
            )
            st.markdown(
                '<div class="dark-card">'
                '<div style="font-size:13px;font-weight:600;color:#C9D1D9;margin-bottom:10px">Your Resume Skills</div>'
                f'<div class="keyword-tags">{tags_html}</div>'
                '</div>',
                unsafe_allow_html=True,
            )


def _save_banner(analysis: Dict[str, Any]) -> None:
    """Prominent save row above the tabs."""
    saved_key = f"top_saved_{id(analysis)}"
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    s_color = "#10B981" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
    grade   = "Great Match!" if score >= 80 else "Good Match" if score >= 60 else "Needs Improvement"

    col_score, col_grade, col_save = st.columns([1, 2, 1])
    with col_score:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;padding:6px 0">'
            f'<span style="font-size:36px;font-weight:800;color:{s_color};line-height:1">{score:.0f}</span>'
            f'<span style="font-size:12px;color:#6E7681">/100</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with col_grade:
        st.markdown(
            f'<div style="padding:6px 0;font-size:14px;font-weight:600;color:#C9D1D9">{grade}</div>',
            unsafe_allow_html=True,
        )
    with col_save:
        if st.session_state.get(saved_key):
            st.markdown(
                '<div style="text-align:center;padding:8px 0;color:#10B981;font-size:12px;font-weight:600">✅ Saved!</div>',
                unsafe_allow_html=True,
            )
        else:
            if st.button("🔖 Save Report", use_container_width=True, key=f"top_save_{id(analysis)}"):
                entry = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "score": score,
                    "analysis": analysis,
                    "has_jd": bool(analysis.get("jd_comparison") or analysis.get("jd_match_analysis")),
                }
                if "saved_reports_list" not in st.session_state:
                    st.session_state["saved_reports_list"] = []
                st.session_state["saved_reports_list"].insert(0, entry)
                st.session_state[saved_key] = True
                # Also mark right-panel save key so it shows saved too
                st.session_state[f"dash_saved_{id(analysis)}"] = True
                st.rerun()
    st.markdown("---")


def display_results_dashboard(analysis: Dict[str, Any]) -> None:
    _save_banner(analysis)
    main_col, right_col = st.columns([3, 1], gap="medium")

    with main_col:
        t1, t2, t3, t4, t5 = st.tabs([
            "🎯 JD Comparison",
            "📊 Score Breakdown",
            "💪 Strengths & Issues",
            "🎓 Skill Validation",
            "🔍 Keywords",
        ])
        with t1:
            _tab_jd_comparison(analysis)
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
            _tab_skills(analysis)
        with t5:
            _tab_keywords_only(analysis)

    with right_col:
        _right_panel(analysis)
