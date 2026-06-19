"""One-time OAuth 2.0 PKCE flow for the X API.

Uses requests-oauthlib's OAuth2Session for the PKCE handshake and token
exchange — the wire format and credential handling are battle-tested across
many OAuth 2.0 providers. We still run a local HTTP server on 127.0.0.1:8765
to capture the redirect.
"""

from __future__ import annotations

import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"

AUTHORIZE_URL = "https://twitter.com/i/oauth2/authorize"
TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
REDIRECT_URI = "http://127.0.0.1:8765/callback"
SCOPES = ["bookmark.read", "tweet.read", "users.read", "offline.access"]
LISTEN_PORT = 8765


class _CallbackHandler(BaseHTTPRequestHandler):
    captured: dict[str, str] = {}
    raw_path: str = ""

    def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler API)
        parsed = urlparse(self.path)
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return
        raw_pairs: dict[str, str] = {}
        for pair in parsed.query.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                raw_pairs[k] = unquote(v)
        if not _CallbackHandler.captured:
            _CallbackHandler.captured.update(raw_pairs)
            _CallbackHandler.raw_path = self.path
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        msg = (
            "Code received. Check the terminal for the final result."
            if "code" in raw_pairs
            else f"Authorization failed: {raw_pairs}"
        )
        self.wfile.write(f"<html><body><h2>{msg}</h2></body></html>".encode())

    def log_message(self, *_args, **_kwargs) -> None:
        pass


def _reset_callback() -> None:
    _CallbackHandler.captured = {}
    _CallbackHandler.raw_path = ""


def _wait_for_callback() -> dict[str, str]:
    """Run a local server until the OAuth redirect arrives; return query params."""
    server = HTTPServer(("127.0.0.1", LISTEN_PORT), _CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        while "code" not in _CallbackHandler.captured and "error" not in _CallbackHandler.captured:
            thread.join(timeout=0.5)
    finally:
        server.shutdown()
    captured = _CallbackHandler.captured
    if "error" in captured:
        raise RuntimeError(f"OAuth error: {captured}")
    if "code" not in captured:
        raise RuntimeError(f"OAuth callback missing code: {captured}")
    return captured


def _exchange_code(
    code: str,
    code_verifier: str,
    client_id: str,
    client_secret: str,
) -> dict:
    """Exchange authorization code for tokens (X requires Basic auth + PKCE)."""
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "code_verifier": code_verifier,
        },
        auth=(client_id, client_secret),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "twitter-analysis/0.1",
        },
        timeout=30,
    )
    if not resp.ok:
        try:
            err = resp.json().get("error", resp.status_code)
        except ValueError:
            err = resp.status_code
        raise RuntimeError(f"({err}) {resp.text}")
    return resp.json()


def _upsert_env(key: str, value: str) -> None:
    lines = ENV_PATH.read_text().splitlines() if ENV_PATH.exists() else []
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            break
    else:
        lines.append(f"{key}={value}")
    tmp = ENV_PATH.with_suffix(".env.tmp")
    tmp.write_text("\n".join(lines) + "\n")
    tmp.replace(ENV_PATH)


def main() -> int:
    if not ENV_PATH.exists():
        print(f"No .env at {ENV_PATH}. Copy .env.example and fill in client credentials first.")
        return 1
    load_dotenv(ENV_PATH)
    client_id = os.environ.get("X_CLIENT_ID", "")
    client_secret = os.environ.get("X_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        print("X_CLIENT_ID and X_CLIENT_SECRET must be set in .env.")
        return 1

    _reset_callback()

    oauth = OAuth2Session(client_id, redirect_uri=REDIRECT_URI, scope=SCOPES)

    code_verifier = oauth._client.create_code_verifier(64)
    code_challenge = oauth._client.create_code_challenge(code_verifier, "S256")

    auth_url, state = oauth.authorization_url(
        AUTHORIZE_URL,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    print(f"Opening browser for authorization. If it doesn't open, visit:\n  {auth_url}\n")
    webbrowser.open(auth_url)

    try:
        callback = _wait_for_callback()
    except RuntimeError as exc:
        print(exc)
        return 1

    if callback.get("state") != state:
        print(
            "State mismatch — you may have approved an old browser tab. "
            "Run authorize again and use only the URL from this run."
        )
        return 1

    print("Got callback. Exchanging for tokens...")

    try:
        token = _exchange_code(
            callback["code"], code_verifier, client_id, client_secret
        )
    except RuntimeError as exc:
        print(f"Token exchange failed: {exc}")
        print(
            "Authorization codes are single-use. Run `twitter-analysis authorize` "
            "again and approve in the browser window opened by that run."
        )
        return 1

    refresh_token = token.get("refresh_token")
    if not refresh_token:
        print(f"No refresh_token in response — did you include 'offline.access' scope? {token}")
        return 1
    _upsert_env("X_REFRESH_TOKEN", refresh_token)

    if not os.environ.get("X_USER_ID"):
        me = requests.get(
            "https://api.x.com/2/users/me",
            headers={
                "Authorization": f"Bearer {token['access_token']}",
                "User-Agent": "twitter-analysis/0.1",
            },
            timeout=30,
        )
        if not me.ok:
            print(
                f"Could not resolve X_USER_ID ({me.status_code}): {me.text}\n"
                "Refresh token was saved, but sync will fail until this is fixed. "
                "Check app permissions (Read) and scopes, then re-run authorize."
            )
            return 1
        user_id = me.json()["data"]["id"]
        _upsert_env("X_USER_ID", user_id)
        print(f"Saved X_USER_ID={user_id}")

    print(f"Saved refresh token to {ENV_PATH}. You can now run `twitter-analysis sync`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
