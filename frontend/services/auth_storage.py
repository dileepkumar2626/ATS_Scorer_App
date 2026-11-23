"""Keep the user signed in across page reloads.

Streamlit forgets st.session_state whenever the page is reloaded, so the Supabase
refresh token is saved in the browser's localStorage. A tiny component
(browser_storage/index.html) reads it back and sends it to Python.

Cookies + st.context.cookies would be simpler, but Streamlit Community Cloud
strips cookies before they reach the app, so that only works locally.
"""
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

REFRESH_KEY = "ra_refresh_token"
VERIFIER_KEY = "ra_oauth_verifier"
_STATE_KEY = "_browser_storage"

_component = components.declare_component(
    "ra_browser_storage", path=str(Path(__file__).parent / "browser_storage")
)


def stored() -> dict | None:
    """Values the browser reported, or None until the component has loaded.

    Read at the top of the script: Streamlit keeps the component's last value in
    session_state, so it's available before the component is drawn again.
    """
    return st.session_state.get(_STATE_KEY)


def sync(writes: dict | None) -> None:
    """Draw the (invisible) component. `writes` = {key: value or None to delete}.

    Pass None to only read; nothing must be written until the saved values have
    been read once, or the empty starting state would wipe them.
    """
    _component(writes=writes, keys=[REFRESH_KEY, VERIFIER_KEY], key=_STATE_KEY, default=None)
