import streamlit as st


def render() -> None:
    st.markdown("""
    <div class="page-header">
      <div class="page-header-icon">📊</div>
      <div>
        <div class="page-header-title">Skill Gap Analysis</div>
        <div class="page-header-sub">
          Visualize skill gaps, track what you have and what you need.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    analysis = st.session_state.get("scorer_analysis") or st.session_state.get("job_match_analysis")

    if not analysis:
        st.markdown("""
        <div class="dark-card" style="text-align:center;padding:48px 32px">
          <div style="font-size:40px;margin-bottom:16px;opacity:.4">📊</div>
          <h3 style="color:var(--text-2)">No Analysis Data Yet</h3>
          <p style="color:var(--text-4);max-width:420px;margin:0 auto">
            Run a resume analysis first. Your skill gap data will appear here automatically
            after each analysis.
          </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎯 Analyze a Resume", use_container_width=True, type="primary"):
                st.session_state.current_view = "scorer"
                st.rerun()
            if st.button("💼 Job Match Analysis", use_container_width=True):
                st.session_state.current_view = "job_match"
                st.rerun()
        return

    # ── Data extraction ─────────────────────────────────────
    details     = analysis.get("skill_validation_details") or {}
    validated   = details.get("validated", [])
    unvalidated = details.get("unvalidated", [])
    total       = details.get("total", len(validated) + len(unvalidated))
    pct         = details.get("validation_pct", 0.0)

    jd = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
    matched_kw  = []
    missing_kw  = []
    skills_gap  = []
    match_pct   = 0
    if jd:
        matched_kw  = jd.get("matched_keywords", []) or []
        missing_kw  = jd.get("missing_keywords",  []) or []
        skills_gap  = jd.get("skills_gap",         []) or []
        match_pct   = float(jd.get("match_percentage", 0))

    # ── Summary metrics ──────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    pct_color = "#10B981" if pct >= 80 else "#F59E0B" if pct >= 60 else "#EF4444"
    mp_color  = "#10B981" if match_pct >= 80 else "#F59E0B" if match_pct >= 60 else "#EF4444"

    c1.metric("Total Skills",      total)
    c2.metric("Validated Skills",  len(validated))
    c3.metric("Unvalidated",       len(unvalidated))
    if jd:
        c4.metric("JD Match",      f"{match_pct:.0f}%")
    else:
        c4.metric("Validation Rate", f"{pct:.0f}%")

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    left, right = st.columns([3, 2], gap="large")

    with left:
        # Skill progress bars
        st.markdown("""
        <div class="dark-card">
          <div style="font-size:14px;font-weight:600;color:var(--text-1);margin-bottom:14px">
            🎓 Skill Validation Breakdown
          </div>
        """, unsafe_allow_html=True)

        prog_cls = "prog-green" if pct >= 80 else "prog-yellow" if pct >= 60 else "prog-red"
        validated_pct = (len(validated) / total * 100) if total else 0
        unvalidated_pct = (len(unvalidated) / total * 100) if total else 0

        st.markdown(f"""
        <div class="prog-wrap">
          <div class="prog-label">
            <span>✅ Validated (backed by evidence)</span>
            <span style="font-weight:700;color:#10B981">{len(validated)}</span>
          </div>
          <div class="prog-track">
            <div class="prog-fill prog-green" style="width:{validated_pct:.1f}%"></div>
          </div>
        </div>
        <div class="prog-wrap" style="margin-top:10px">
          <div class="prog-label">
            <span>⚠️ Unvalidated (listed only)</span>
            <span style="font-weight:700;color:#F59E0B">{len(unvalidated)}</span>
          </div>
          <div class="prog-track">
            <div class="prog-fill prog-yellow" style="width:{unvalidated_pct:.1f}%"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if jd and skills_gap:
            gap_pct = min(len(skills_gap) / max(len(skills_gap) + len(validated), 1) * 100, 100)
            st.markdown(f"""
            <div class="prog-wrap" style="margin-top:10px">
              <div class="prog-label">
                <span>❌ Skills from JD you're missing</span>
                <span style="font-weight:700;color:#EF4444">{len(skills_gap)}</span>
              </div>
              <div class="prog-track">
                <div class="prog-fill prog-red" style="width:{min(gap_pct,100):.1f}%"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Validated skills
        if validated:
            v_tags = "".join(
                f'<span class="kw-tag kw-matched">✓ {e.get("skill","?") if isinstance(e, dict) else e}</span>'
                for e in validated
            )
            st.markdown(f"""
            <div class="dark-card" style="margin-top:14px">
              <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:10px">
                ✅ Validated Skills — Backed by Project Evidence
              </div>
              <div class="keyword-tags">{v_tags}</div>
            </div>
            """, unsafe_allow_html=True)

        # Unvalidated skills
        if unvalidated:
            u_tags = "".join(
                f'<span class="kw-tag kw-partial">! {s}</span>' for s in unvalidated
            )
            st.markdown(f"""
            <div class="dark-card" style="margin-top:14px">
              <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:6px">
                ⚠️ Unvalidated Skills — Add Project Evidence
              </div>
              <div style="font-size:12px;color:var(--text-4);margin-bottom:10px">
                These are listed in your resume but not backed by any project or experience bullet.
              </div>
              <div class="keyword-tags">{u_tags}</div>
            </div>
            """, unsafe_allow_html=True)

    with right:
        # JD skills gap
        if jd:
            st.markdown(f"""
            <div class="dark-card-sm">
              <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:10px">
                🎯 JD Match Rate
              </div>
              <div style="text-align:center;margin-bottom:12px">
                <span style="font-size:36px;font-weight:800;color:{mp_color}">{match_pct:.0f}%</span>
              </div>
              <div class="prog-track" style="height:10px">
                <div class="prog-fill {'prog-green' if match_pct>=80 else 'prog-yellow' if match_pct>=60 else 'prog-red'}"
                     style="width:{match_pct:.1f}%"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            if skills_gap:
                rows_html = "".join(
                    f'<div class="skill-row"><span>{s}</span>'
                    f'<span class="priority-{"high" if i < 2 else "medium" if i < 4 else "low"}">'
                    f'{"High" if i < 2 else "Medium" if i < 4 else "Low"}</span></div>'
                    for i, s in enumerate(skills_gap[:8])
                )
                st.markdown(f"""
                <div class="dark-card-sm" style="margin-top:12px">
                  <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:10px">
                    🧩 Skills Gap from JD
                  </div>
                  {rows_html}
                </div>
                """, unsafe_allow_html=True)

            if missing_kw:
                tags = "".join(
                    f'<span class="kw-tag kw-missing">✗ {k}</span>' for k in missing_kw[:12]
                )
                st.markdown(f"""
                <div class="dark-card-sm" style="margin-top:12px">
                  <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:10px">
                    ❌ Missing Keywords
                  </div>
                  <div class="keyword-tags">{tags}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            # No JD — show improvement tips
            st.markdown("""
            <div class="dark-card-sm">
              <div style="font-size:13px;font-weight:600;color:var(--text-2);margin-bottom:10px">
                💡 Improve Your Skill Gap Score
              </div>
              <div class="reco-item">
                <div class="reco-dot reco-medium">1</div>
                <span>Add a job description in <strong>Job Match</strong> for a detailed gap analysis.</span>
              </div>
              <div class="reco-item">
                <div class="reco-dot reco-medium">2</div>
                <span>For each unvalidated skill, add a project bullet mentioning it by name.</span>
              </div>
              <div class="reco-item">
                <div class="reco-dot reco-medium">3</div>
                <span>Quantify your work: "Built X using Y, achieving Z% improvement."</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Footer CTA
    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Re-analyze Resume", use_container_width=True):
            st.session_state.current_view = "scorer"
            st.rerun()
    with col2:
        if st.button("💼 Run Job Match Analysis", use_container_width=True, type="primary"):
            st.session_state.current_view = "job_match"
            st.rerun()
