import os
from flask import session, redirect, url_for
from requests_oauthlib import OAuth2Session

# Configuration for Google OAuth2
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
GOOGLE_SCOPE = ["openid", "email", "profile"]

def get_google_oauth2_session(state=None, token=None):
    """Create an OAuth2Session for Google authentication."""
    redirect_uri = url_for("auth_callback", _external=True)
    return OAuth2Session(
        client_id=GOOGLE_CLIENT_ID,
        redirect_uri=redirect_uri,
        scope=GOOGLE_SCOPE,
        state=state,
        token=token
    )

def get_google_auth_url():
    """Get the Google OAuth2 authorization URL."""
    google = get_google_oauth2_session()
    auth_url, state = google.authorization_url(
        GOOGLE_AUTHORIZATION_BASE_URL,
        access_type="offline",
        prompt="select_account"
    )
    session["oauth_state"] = state
    return auth_url

def fetch_google_token():
    """Fetch the OAuth2 token from Google after user authorization."""
    google = get_google_oauth2_session(state=session.get("oauth_state"))
    token = google.fetch_token(
        GOOGLE_TOKEN_URL,
        client_secret=GOOGLE_CLIENT_SECRET,
        authorization_response=url_for("auth_callback", _external=True)
    )
    session["oauth_token"] = token
    return token

def get_google_user_info():
    """Retrieve user information from Google using the OAuth2 token."""
    google = get_google_oauth2_session(token=session.get("oauth_token"))
    resp = google.get(GOOGLE_USER_INFO_URL)
    return resp.json()