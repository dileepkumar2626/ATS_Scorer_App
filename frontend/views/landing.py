import streamlit as st


def render():
    # Hero section
    st.markdown("""
    <div class="hero-section">
      <div class="hero-title">
        AI-Powered<br><span>Resume Analyzer</span>
      </div>
      <p class="hero-sub">
        Get instant ATS scores, keyword matching, skill validation, and actionable
        recommendations to land more interviews.
      </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Analyze My Resume Now", use_container_width=True, type="primary"):
            st.session_state.current_view = "scorer"
            st.rerun()

    st.markdown("<div style='margin-top:40px'></div>", unsafe_allow_html=True)

    # Stats row
    s1, s2, s3, s4 = st.columns(4)
    for col, num, label in [
        (s1, "10K+",  "Resumes Analyzed"),
        (s2, "87%",   "Avg. Score Improvement"),
        (s3, "5",     "Scoring Dimensions"),
        (s4, "< 30s", "Analysis Time"),
    ]:
        col.markdown(f"""
        <div class="stat-box">
          <div class="stat-number">{num}</div>
          <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:36px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:20px;font-weight:700;color:var(--text-1);margin-bottom:20px">
      ✨ Key Features
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    for col, icon, title, desc in [
        (f1, "📊", "Comprehensive Scoring",
         "Get detailed scores across 5 dimensions: Formatting, Keywords, Content Quality, Skill Validation, and ATS Compatibility."),
        (f2, "🔍", "Keyword Analysis",
         "See exactly which keywords match the job description and which ones are missing — with green/red tags."),
        (f3, "✅", "Skill Validation",
         "AI verifies your claimed skills are actually demonstrated in your projects and experience. No more empty claims."),
    ]:
        with col:
            st.markdown(f"""
            <div class="feature-card">
              <div class="feature-icon">{icon}</div>
              <div class="feature-title">{title}</div>
              <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    f4, f5, f6 = st.columns(3)
    for col, icon, title, desc in [
        (f4, "💼", "Job Description Match",
         "Upload a job description to see how well your resume aligns with the specific role you're targeting."),
        (f5, "💡", "Actionable Recommendations",
         "Get prioritized, specific tips to improve your ATS score — sorted from critical to low priority."),
        (f6, "📑", "PDF Export",
         "Download a full PDF report of your analysis to share with mentors or track your progress over time."),
    ]:
        with col:
            st.markdown(f"""
            <div class="feature-card">
              <div class="feature-icon">{icon}</div>
              <div class="feature-title">{title}</div>
              <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:36px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:20px;font-weight:700;color:var(--text-1);margin-bottom:20px">
      🚀 How It Works
    </div>
    """, unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3)
    for col, num, title, desc in [
        (h1, "1", "Upload Your Resume",
         "Drop your PDF or DOCX resume. Supported up to 5 MB."),
        (h2, "2", "AI Analyzes Everything",
         "Our AI parses, scores, and matches your resume across all dimensions in under 30 seconds."),
        (h3, "3", "Get Actionable Insights",
         "Review your score, keyword matches, and prioritized recommendations to improve."),
    ]:
        with col:
            st.markdown(f"""
            <div class="dark-card" style="text-align:center;padding:28px 20px">
              <div style="width:48px;height:48px;border-radius:50%;background:var(--purple-gradient);
                   display:flex;align-items:center;justify-content:center;font-size:20px;
                   font-weight:800;color:white;margin:0 auto 14px">{num}</div>
              <div style="font-size:15px;font-weight:600;color:var(--text-1);margin-bottom:6px">
                {title}
              </div>
              <div style="font-size:13px;color:var(--text-3)">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:32px;text-align:center'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Get Started — It's Free", use_container_width=True, type="primary"):
            st.session_state.current_view = "scorer"
            st.rerun()
