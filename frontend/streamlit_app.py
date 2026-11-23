import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="ResumeAnalyzer AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session defaults ────────────────────────────────────────
for key, default in [
    ("access_token",         None),
    ("refresh_token",        None),
    ("user_id",              None),
    ("user_email",           None),
    ("auth_error",           None),
    ("auth_info",            None),
    ("current_view",         "landing"),
    ("show_forgot_password", False),
    ("saved_reports_list",   []),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Restore sign-in (OAuth callback, or saved cookie after a reload) ─────
from frontend.services import auth_cookies


def _set_user(result: dict) -> None:
    st.session_state.access_token  = result["access_token"]
    st.session_state.refresh_token = result["refresh_token"]
    st.session_state.user_id       = result["user_id"]
    st.session_state.user_email    = result["email"]


if not st.session_state.access_token and "code" in st.query_params:
    from frontend.services import supabase_client
    st.session_state._restore_attempted = True
    result = supabase_client.exchange_code_for_session(
        st.query_params["code"],
        auth_cookies.get(auth_cookies.VERIFIER_COOKIE),
    )
    st.query_params.clear()
    if "error" in result:
        st.session_state.auth_error = f"Google sign-in failed: {result['error']}"
    else:
        _set_user(result)
        st.rerun()

# Cookies are only read once per browser session; after "Sign out" the stale
# cookie value must not sign the user straight back in.
if not st.session_state.get("_restore_attempted"):
    st.session_state._restore_attempted = True
    saved_token = auth_cookies.get(auth_cookies.REFRESH_COOKIE)
    if saved_token and not st.session_state.access_token:
        from frontend.services import supabase_client
        result = supabase_client.restore_session(saved_token)
        if "error" not in result:
            _set_user(result)


# ── Load CSS ────────────────────────────────────────────────
def load_css():
    try:
        css_path = Path(__file__).parent / "assets" / "styles.css"
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        # <link> tags are more reliable than CSS @import for external fonts in Streamlit
        return f"<style>{css}</style>"
    except FileNotFoundError:
        return ""

st.markdown(load_css(), unsafe_allow_html=True)


# ── Nav helper ──────────────────────────────────────────────
def _nav_item(icon: str, label: str, view_key: str):
    """Active = styled div, inactive = clickable button."""
    if st.session_state.current_view == view_key:
        st.sidebar.markdown(
            f'<div class="nav-active"><span>{icon}</span><span>{label}</span></div>',
            unsafe_allow_html=True,
        )
        return False
    else:
        clicked = st.sidebar.button(
            f"{icon}  {label}", key=f"nav_{view_key}", use_container_width=True
        )
        if clicked:
            st.session_state.current_view = view_key
            st.rerun()
        return clicked


# ── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    from frontend.services import supabase_client

    # ── Brand ────────────────────────────────────────────────
    st.markdown(
        '<div class="nav-brand">'
        '<div class="brand-icon">📋</div>'
        '<div>ResumeAnalyzer <span style="color:#A78BFA">AI</span></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Account / Auth (at top) ──────────────────────────────
    if st.session_state.access_token:
        email_display = st.session_state.user_email or "User"
        initial = email_display[0].upper() if email_display else "U"
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;padding:8px 4px 12px;'
            f'background:rgba(255,255,255,.04);border-radius:10px;margin-bottom:4px">'
            f'<div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#7C3AED,#4F46E5);'
            f'display:flex;align-items:center;justify-content:center;font-weight:700;'
            f'font-size:14px;color:white;flex-shrink:0;box-shadow:0 2px 8px rgba(124,58,237,.4)">{initial}</div>'
            f'<div style="overflow:hidden;min-width:0">'
            f'<div style="font-size:10.5px;color:#64748B;margin-bottom:1px;font-weight:500;text-transform:uppercase;letter-spacing:.04em">Account</div>'
            f'<div style="font-size:12.5px;color:#CBD5E1;font-weight:500;'
            f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:155px">{email_display}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
        if st.button("Sign out", use_container_width=True):
            supabase_client.sign_out(st.session_state.access_token)
            for k in ("access_token", "refresh_token", "user_id", "user_email"):
                st.session_state[k] = None
            st.rerun()

    else:
        # Auth errors / info banners
        if st.session_state.auth_error:
            st.error(st.session_state.auth_error)
            st.session_state.auth_error = None
        if st.session_state.auth_info:
            st.info(st.session_state.auth_info)
            st.session_state.auth_info = None

        tab_in, tab_up = st.tabs(["Sign in", "Sign up"])

        # ── Sign in ──────────────────────────────────────────
        with tab_in:
            if st.session_state.show_forgot_password:
                st.markdown("**🔑 Reset Password**")
                fp_email = st.text_input("Your email address", key="fp_email")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Send Reset Email", use_container_width=True, type="primary"):
                        if fp_email:
                            result = supabase_client.reset_password_for_email(fp_email)
                            if "error" in result:
                                st.session_state.auth_error = result["error"]
                            else:
                                st.session_state.auth_info = (
                                    "Password reset email sent! Check your inbox."
                                )
                                st.session_state.show_forgot_password = False
                            st.rerun()
                        else:
                            st.warning("Please enter your email.")
                with c2:
                    if st.button("← Back", use_container_width=True):
                        st.session_state.show_forgot_password = False
                        st.rerun()
            else:
                with st.form("signin_form", clear_on_submit=False):
                    email    = st.text_input("Email",    key="signin_email")
                    password = st.text_input("Password", type="password", key="signin_pw")
                    submitted = st.form_submit_button("Sign in", use_container_width=True)

                if submitted:
                    result = supabase_client.sign_in_with_password(email, password)
                    if "error" in result:
                        st.session_state.auth_error = result["error"]
                    else:
                        _set_user(result)
                    st.rerun()

                if st.button("Forgot password?", key="forgot_pw_btn"):
                    st.session_state.show_forgot_password = True
                    st.rerun()

        # ── Sign up ──────────────────────────────────────────
        with tab_up:
            with st.form("signup_form", clear_on_submit=False):
                email_up    = st.text_input("Email",             key="signup_email")
                password_up = st.text_input("Password (min 6)", type="password", key="signup_pw")
                submitted_up = st.form_submit_button("Create account", use_container_width=True)

            if submitted_up:
                result = supabase_client.sign_up_with_password(email_up, password_up)
                if "error" in result:
                    st.session_state.auth_error = result["error"]
                elif result.get("pending_confirmation"):
                    st.session_state.auth_info = (
                        f"Check your inbox — confirmation email sent to {result['email']}."
                    )
                else:
                    _set_user(result)
                st.rerun()

        # Google OAuth — branded button
        st.markdown(
            '<div style="display:flex;align-items:center;gap:10px;margin:10px 0 4px">'
            '<div style="flex:1;height:1px;background:rgba(255,255,255,.07)"></div>'
            '<div style="font-size:11px;color:#64748B;font-weight:500">or</div>'
            '<div style="flex:1;height:1px;background:rgba(255,255,255,.07)"></div>'
            '</div>',
            unsafe_allow_html=True,
        )
        oauth = supabase_client.google_oauth_url()
        if "error" in oauth:
            st.caption(f"Google sign-in unavailable: {oauth['error']}")
        else:
            st.markdown(f"""
            <a href="{oauth['url']}" class="google-btn" target="_blank">
              <svg class="google-logo" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                <path fill="none" d="M0 0h48v48H0z"/>
              </svg>
              Continue with Google
            </a>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Navigation (below auth) ──────────────────────────────
    st.markdown('<div class="nav-section-label">Main</div>', unsafe_allow_html=True)
    _nav_item("🎯", "Analyze Resume", "scorer")
    _nav_item("💼", "Job Match",      "job_match")
    _nav_item("📊", "Skill Gap",      "skill_gap")

    st.markdown('<div class="nav-section-label">Tools</div>', unsafe_allow_html=True)
    _nav_item("📝", "Resume Builder", "builder")
    _nav_item("🕐", "History",        "history")
    _nav_item("🔖", "Saved Reports",  "saved_reports")

    st.markdown('<div class="nav-section-label">Other</div>', unsafe_allow_html=True)
    _nav_item("🏠", "Home", "landing")

    # Pro upgrade card
    st.markdown("""
    <div class="pro-card">
      <div class="pro-title">👑 Pro</div>
      <div class="pro-desc">Unlock unlimited analysis, advanced insights & research reports.</div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Upgrade →", key="upgrade_btn", use_container_width=True, type="primary")

    # Save / clear the browser cookies that keep the user signed in on reload.
    auth_cookies.sync({
        auth_cookies.REFRESH_COOKIE:  st.session_state.refresh_token,
        auth_cookies.VERIFIER_COOKIE: None if st.session_state.access_token
                                      else st.session_state.get("_google_code_verifier"),
    })


# ── View routing ────────────────────────────────────────────
view = st.session_state.current_view

if view == "landing":
    from frontend.views import landing
    landing.render()

elif view == "scorer":
    from frontend.views import scorer
    scorer.render()

elif view == "job_match":
    from frontend.views import job_match
    job_match.render()

elif view == "history":
    from frontend.views import history
    history.render()

elif view == "skill_gap":
    from frontend.views import skill_gap
    skill_gap.render()

elif view == "builder":
    from frontend.views import builder
    builder.render()

elif view == "saved_reports":
    from frontend.views import saved_reports
    saved_reports.render()