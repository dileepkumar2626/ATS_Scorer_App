"""Keep the user signed in across page reloads.

Streamlit forgets st.session_state whenever the page is reloaded, so the Supabase
refresh token is also saved in a browser cookie. On the first run of a new session
the app reads it back (st.context.cookies) and exchanges it for a fresh session.
"""
import json
from urllib.parse import unquote

import streamlit as st
import streamlit.components.v1 as components

REFRESH_COOKIE = "ra_refresh_token"
VERIFIER_COOKIE = "ra_oauth_verifier"
MAX_AGE_SECONDS = 60 * 60 * 24 * 30  # stay signed in for 30 days


def get(name: str) -> str:
    """Cookie value sent by the browser when this session started ('' if none)."""
    try:
        return unquote(st.context.cookies.get(name) or "")
    except Exception:
        return ""


def sync(cookies: dict) -> None:
    """Write each {name: value} to the browser; a value of None deletes the cookie.

    Rendered on every run. Streamlit only re-executes the script when its content
    changes (e.g. the refresh token rotated), so this is cheap.
    """
    payload = json.dumps(cookies)
    components.html(
        f"""
<script>
(function () {{
  const doc = window.parent.document;
  const secure = window.parent.location.protocol === "https:" ? "; Secure" : "";
  const cookies = {payload};
  for (const [name, value] of Object.entries(cookies)) {{
    if (value) {{
      doc.cookie = name + "=" + encodeURIComponent(value) +
        "; path=/; max-age={MAX_AGE_SECONDS}; SameSite=Lax" + secure;
    }} else {{
      doc.cookie = name + "=; path=/; max-age=0; SameSite=Lax" + secure;
    }}
  }}
}})();
</script>
""",
        height=0,
    )
