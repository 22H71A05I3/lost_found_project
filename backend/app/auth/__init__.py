# Flask blueprint for Google OAuth 2.0 login, logout, and user profile session
from flask import Blueprint, redirect, url_for, session, request
from oauthlib.oauth2 import WebApplicationClient
import requests
import os

auth_bp = Blueprint('auth', __name__)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@auth_bp.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url.replace("/login", "/callback"),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(token_response.text)
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    userinfo = userinfo_response.json()
    session["user"] = {
        "email": userinfo["email"],
        "name": userinfo["name"],
        "picture": userinfo["picture"]
    }
    return redirect(url_for("profile"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@auth_bp.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return session["user"]