import os
import logging
from pathlib import Path
from typing import Any, Dict
import streamlit as st
from supabase import Client, ClientOptions, create_client

logger = logging.getLogger('ats_resume_scorer')


try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / '.env')
except ImportError:
    pass


def _secret(key: str, section: str = 'supabase') -> str:
    """Read from env first, then fall back to st.secrets[section][key]."""
    val = os.getenv(key, '')
    if val:
        return val
    try:
        return st.secrets[section][key]
    except (KeyError, FileNotFoundError, AttributeError):
        return ''


SUPABASE_URL = _secret('SUPABASE_URL')
SUPABASE_ANON_KEY = _secret('SUPABASE_ANON_KEY')

OAUTH_REDIRECT_URL = (
    os.getenv('AUTH_REDIRECT_URL')
    or _secret('AUTH_REDIRECT_URL', 'supabase')
    or _secret('redirect_uri', 'google_oauth')
    or 'https://atsscorerapp-bn6rwhcjax6iwts4vax8ss.streamlit.app'
)


def _missing_config() -> str | None:
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return 'Supabase is not configured — set SUPABASE_URL and SUPABASE_ANON_KEY in .env or .streamlit/secrets.toml'
    return None


def get_client() -> Client | None:
    """A fresh, per-call client.

    The client is deliberately NOT shared (no @st.cache_resource). A shared client
    stores whichever user signed in last and silently refreshes *their* tokens in a
    background timer. That rotates the refresh token kept in the user's browser
    cookie and logs them out on the next reload, and a shared sign_out() could
    sign out a different user. Each call gets its own client with auto-refresh off.
    """
    if _missing_config():
        return None
    return create_client(
        SUPABASE_URL,
        SUPABASE_ANON_KEY,
        options=ClientOptions(auto_refresh_token=False, persist_session=False, flow_type='pkce'),
    )


def _session_dict(session, user) -> Dict[str, Any]:
    return {
        'access_token':  session.access_token,
        'refresh_token': session.refresh_token,
        'user_id':       user.id,
        'email':         user.email,
    }


def sign_in_with_password(email: str, password: str) -> Dict[str, Any]:
    err = _missing_config()
    if err:
        return {'error': err}
    try:
        resp = get_client().auth.sign_in_with_password(
            {'email': email, 'password': password}
        )
        if not resp.session or not resp.user:
            return {'error': 'Invalid credentials'}
        return _session_dict(resp.session, resp.user)
    except Exception as exc:
        logger.warning(f'sign_in_with_password failed: {exc}')
        return {'error': _humanize(exc)}


def sign_up_with_password(email: str, password: str) -> Dict[str, Any]:
    err = _missing_config()
    if err:
        return {'error': err}
    try:
        resp = get_client().auth.sign_up({'email': email, 'password': password})
        if resp.session and resp.user:
            return _session_dict(resp.session, resp.user)
        if resp.user:
            return {'pending_confirmation': True, 'email': email}
        return {'error': 'Sign-up failed'}
    except Exception as exc:
        logger.warning(f'sign_up failed: {exc}')
        return {'error': _humanize(exc)}


def google_oauth_url() -> Dict[str, Any]:
    err = _missing_config()
    if err:
        return {'error': err}
    # The sidebar calls this on every rerun, so cache the URL + PKCE verifier in
    # session_state; a new verifier on each rerun would no longer match the URL.
    # The verifier is also written to a browser cookie by streamlit_app.py, because
    # the Google button opens a new tab (a new Streamlit session) for the callback.
    if '_google_oauth_cache' in st.session_state and st.session_state.get('_google_code_verifier'):
        return {'url': st.session_state['_google_oauth_cache']}
    try:
        client = get_client()
        resp = client.auth.sign_in_with_oauth({
            'provider': 'google',
            'options': {'redirect_to': OAUTH_REDIRECT_URL},
        })
        try:
            storage_key = f'{client.auth._storage_key}-code-verifier'
            cv = (client.auth._storage.get_item(storage_key) or '').partition('/')[0]
        except Exception:
            cv = ''
        st.session_state['_google_oauth_cache'] = resp.url
        st.session_state['_google_code_verifier'] = cv
        return {'url': resp.url}
    except Exception as exc:
        logger.warning(f'oauth url generation failed: {exc}')
        return {'error': _humanize(exc)}


def exchange_code_for_session(auth_code: str, code_verifier: str = '') -> Dict[str, Any]:
    """Called once after the OAuth provider redirects back with `?code=...`.

    `code_verifier` comes from the browser cookie set when the Google button was
    shown; session_state is the fallback when the callback lands in the same tab.
    """
    err = _missing_config()
    if err:
        return {'error': err}
    code_verifier = code_verifier or st.session_state.get('_google_code_verifier', '')
    if not code_verifier:
        return {'error': 'Sign-in link expired. Please click "Continue with Google" again.'}
    try:
        resp = get_client().auth.exchange_code_for_session({
            'auth_code':     auth_code,
            'code_verifier': code_verifier,
            'redirect_to':   OAUTH_REDIRECT_URL,
        })
        if not resp.session or not resp.user:
            return {'error': 'OAuth exchange returned no session'}
        # Clear cached URL so the next sign-in attempt generates a fresh PKCE pair
        st.session_state.pop('_google_oauth_cache', None)
        st.session_state.pop('_google_code_verifier', None)
        return _session_dict(resp.session, resp.user)
    except Exception as exc:
        logger.warning(f'exchange_code_for_session failed: {exc}')
        return {'error': _humanize(exc)}


def restore_session(refresh_token: str) -> Dict[str, Any]:
    """Turn the refresh token saved in the browser cookie into a fresh session.

    Supabase rotates refresh tokens, so the caller must save the new one.
    """
    err = _missing_config()
    if err:
        return {'error': err}
    if not refresh_token:
        return {'error': 'No saved session'}
    try:
        resp = get_client().auth.refresh_session(refresh_token)
        if not resp.session or not resp.user:
            return {'error': 'Saved session is no longer valid'}
        return _session_dict(resp.session, resp.user)
    except Exception as exc:
        logger.info(f'restore_session failed: {exc}')
        return {'error': _humanize(exc)}


def reset_password_for_email(email: str) -> Dict[str, Any]:
    err = _missing_config()
    if err:
        return {'error': err}
    try:
        get_client().auth.reset_password_for_email(
            email,
            {'redirect_to': OAUTH_REDIRECT_URL}
        )
        return {'success': True}
    except Exception as exc:
        logger.warning(f'reset_password failed: {exc}')
        return {'error': _humanize(exc)}


def sign_out(access_token: str | None = None) -> None:
    """Revoke this browser's session only (scope='local'), using the user's own token."""
    if _missing_config() or not access_token:
        return
    try:
        get_client().auth.admin.sign_out(access_token, 'local')
    except Exception as exc:
        logger.warning(f'sign_out failed: {exc}')


def _humanize(exc: Exception) -> str:
    msg = str(exc)
    # supabase errors arrive as "<status>: {json blob}" — surface the human bit
    if 'invalid_grant' in msg.lower() or 'invalid login' in msg.lower():
        return 'Wrong email or password'
    if 'user already registered' in msg.lower() or 'already been registered' in msg.lower():
        return 'An account with this email already exists — try signing in'
    if 'password should be at least' in msg.lower():
        return 'Password too short (Supabase default is 6 characters)'
    return msg
