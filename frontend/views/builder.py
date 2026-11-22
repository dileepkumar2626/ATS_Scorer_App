import streamlit as st


BUILDERS = [
    {
        "name": "FlowCV",
        "url":  "https://flowcv.com",
        "icon": "🌊",
        "desc": "Free, beautiful resume templates. Drag-and-drop builder with ATS-friendly designs. The most popular choice.",
        "badge": "Most Popular",
        "badge_cls": "badge-green",
    },
    {
        "name": "Resume.io",
        "url":  "https://resume.io",
        "icon": "📄",
        "desc": "Professional templates with real-time preview. Great for creative and corporate roles.",
        "badge": "Premium",
        "badge_cls": "badge-purple",
    },
    {
        "name": "Zety",
        "url":  "https://zety.com/resume-builder",
        "icon": "⚡",
        "desc": "AI-powered resume builder with keyword suggestions and expert tips built in.",
        "badge": "AI-Powered",
        "badge_cls": "badge-blue",
    },
    {
        "name": "Canva Resume",
        "url":  "https://www.canva.com/resumes/templates",
        "icon": "🎨",
        "desc": "Visually stunning templates. Best for design, marketing, or creative roles.",
        "badge": "Visual",
        "badge_cls": "badge-yellow",
    },
    {
        "name": "Novoresume",
        "url":  "https://novoresume.com",
        "icon": "📋",
        "desc": "Smart resume builder with ATS optimization, content analyzer, and cover letter maker.",
        "badge": "ATS-Focused",
        "badge_cls": "badge-green",
    },
    {
        "name": "LinkedIn Resume",
        "url":  "https://www.linkedin.com/resume-builder",
        "icon": "🔗",
        "desc": "Build a resume directly from your LinkedIn profile in one click.",
        "badge": "LinkedIn",
        "badge_cls": "badge-blue",
    },
]

ATS_TIPS = [
    ("📐", "Use Standard Sections", "Contact Info, Summary, Experience, Education, Skills — in this order. ATS systems expect these."),
    ("🔤", "No Tables or Columns",  "Single-column layout only. Tables and multi-column designs break most ATS parsers."),
    ("📝", "Standard Fonts Only",   "Calibri, Arial, Times New Roman, or Helvetica. Fancy fonts may not parse correctly."),
    ("📏", "File Format Matters",   "Save as .docx or single-column PDF. DOCX is safest for ATS compatibility."),
    ("🏷️", "Match JD Keywords",     "Mirror the exact phrases from the job description — ATS matches keywords precisely."),
    ("📊", "Quantify Everything",   "\"Improved accuracy by 23%\" scores higher than \"improved accuracy\". Add numbers."),
]


def render() -> None:
    st.markdown("""
    <div class="page-header">
      <div class="page-header-icon">📝</div>
      <div>
        <div class="page-header-title">Resume Builder</div>
        <div class="page-header-sub">
          Build a professional ATS-friendly resume with these recommended tools.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Score CTA if analysis available
    analysis = st.session_state.get("scorer_analysis") or st.session_state.get("job_match_analysis")
    if analysis:
        score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
        color = "#10B981" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
        st.markdown(f"""
        <div class="dark-card" style="border-color:rgba(124,58,237,.4);margin-bottom:20px">
          <div style="display:flex;align-items:center;gap:14px">
            <div style="text-align:center;min-width:70px">
              <div style="font-size:30px;font-weight:800;color:{color}">{score:.0f}</div>
              <div style="font-size:11px;color:var(--text-4)">Current Score</div>
            </div>
            <div>
              <div style="font-size:14px;font-weight:600;color:var(--text-1);margin-bottom:4px">
                Use these tools to build a better resume, then re-analyze it.
              </div>
              <div style="font-size:12px;color:var(--text-3)">
                Your analysis results are saved — after rebuilding, upload again and compare.
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Builder cards
    st.markdown("""
    <div style="font-size:16px;font-weight:700;color:var(--text-1);margin-bottom:14px">
      🛠️ Recommended Resume Builders
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, b in enumerate(BUILDERS):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card" style="margin-bottom:12px">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
                <div style="font-size:22px">{b['icon']}</div>
                <span class="badge {b['badge_cls']}" style="font-size:10px">{b['badge']}</span>
              </div>
              <div class="feature-title">{b['name']}</div>
              <div class="feature-desc">{b['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.link_button(f"Open {b['name']} →", url=b["url"], use_container_width=True)

    st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)

    # ATS tips
    st.markdown("""
    <div style="font-size:16px;font-weight:700;color:var(--text-1);margin-bottom:14px">
      💡 ATS-Friendly Resume Tips
    </div>
    """, unsafe_allow_html=True)

    tip_rows = [ATS_TIPS[i:i+2] for i in range(0, len(ATS_TIPS), 2)]
    for row in tip_rows:
        cols = st.columns(2)
        for col, (icon, title, desc) in zip(cols, row):
            with col:
                st.markdown(f"""
                <div class="dark-card-sm" style="margin-bottom:10px">
                  <div style="display:flex;align-items:flex-start;gap:10px">
                    <div style="font-size:20px;flex-shrink:0">{icon}</div>
                    <div>
                      <div style="font-size:13px;font-weight:600;color:var(--text-1);margin-bottom:3px">{title}</div>
                      <div style="font-size:12px;color:var(--text-3);line-height:1.5">{desc}</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Analyze Your New Resume", use_container_width=True, type="primary"):
            st.session_state.current_view = "scorer"
            st.rerun()
