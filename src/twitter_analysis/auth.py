"""OAuth 2.0 token refresh for the X API.

The authorize.py script handles the one-time PKCE flow and writes the initial
refresh token to .env. After that, get_access_token() exchanges that refresh
token for a fresh access token on every run. X rotates refresh tokens on each
refresh, so the new one is persisted back to .env before being used.
"""

from __future__ import annotations

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
ME_URL = "https://api.x.com/2/users/me"
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def _read_env() -> dict[str, str]:
    load_dotenv(ENV_PATH, override=True)
    required = ["X_CLIENT_ID", "X_CLIENT_SECRET", "X_REFRESH_TOKEN"]
    env = {k: os.environ.get(k, "") for k in required}
    env["X_USER_ID"] = os.environ.get("X_USER_ID", "")
    missing = [k for k in required if not env[k]]
    if missing:
        raise RuntimeError(
            f"Missing required env vars: {', '.join(missing)}. "
            "Run `twitter-analysis authorize` first."
        )
    return env


def _write_env_key(key: str, value: str) -> None:
    """Atomically update a single key in .env without disturbing other lines."""
    lines = ENV_PATH.read_text().splitlines() if ENV_PATH.exists() else []
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            found = True
            break
    if not found:
        lines.append(f"{key}={value}")
    tmp = ENV_PATH.with_suffix(".env.tmp")
    tmp.write_text("\n".join(lines) + "\n")
    tmp.replace(ENV_PATH)


def _write_refresh_token(new_token: str) -> None:
    _write_env_key("X_REFRESH_TOKEN", new_token)


def _resolve_user_id(access_token: str, env: dict[str, str]) -> str:
    """Return X_USER_ID from env, or fetch from /users/me and persist it."""
    user_id = env.get("X_USER_ID", "")
    if user_id:
        return user_id
    me = requests.get(
        ME_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "twitter-analysis/0.1",
        },
        timeout=30,
    )
    if not me.ok:
        raise RuntimeError(
            f"Could not resolve X_USER_ID ({me.status_code}): {me.text}. "
            "Re-run `twitter-analysis authorize`."
        )
    user_id = me.json()["data"]["id"]
    _write_env_key("X_USER_ID", user_id)
    return user_id


def get_access_token() -> tuple[str, str]:
    """Refresh and return (access_token, user_id).

    Persists the rotated refresh token to .env before returning so a crash
    after this point can't strand us with a stale token.
    """
    env = _read_env()
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": env["X_REFRESH_TOKEN"],
            "client_id": env["X_CLIENT_ID"],
        },
        auth=(env["X_CLIENT_ID"], env["X_CLIENT_SECRET"]),
        headers={"User-Agent": "twitter-analysis/0.1"},
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(
            f"Token refresh failed ({resp.status_code}): {resp.text}. "
            "Refresh token may be expired or revoked — re-run "
            "`twitter-analysis authorize`."
        )
    payload = resp.json()
    new_refresh = payload.get("refresh_token")
    if new_refresh and new_refresh != env["X_REFRESH_TOKEN"]:
        _write_refresh_token(new_refresh)
    access_token = payload["access_token"]
    user_id = _resolve_user_id(access_token, env)
    return access_token, user_id
