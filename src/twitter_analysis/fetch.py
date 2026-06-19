"""Bookmarks API client.

Calls GET /2/users/:id/bookmarks with the field expansions needed to
fully reconstruct each bookmark — including Twitter Articles (the rich
long-form post type, surfaced via tweet.fields=article) and long tweets
(tweet.fields=note_tweet). Pagination stops early once a known since_id
is reached, since results come back newest-first.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any

import requests

BOOKMARKS_URL = "https://api.x.com/2/users/{user_id}/bookmarks"

TWEET_FIELDS = ",".join(
    [
        "article",
        "note_tweet",
        "created_at",
        "entities",
        "attachments",
        "public_metrics",
        "referenced_tweets",
        "text",
        "lang",
        "author_id",
    ]
)
EXPANSIONS = ",".join(["author_id", "attachments.media_keys", "referenced_tweets.id"])
USER_FIELDS = "name,username,verified"
MEDIA_FIELDS = "url,preview_image_url,type,alt_text"

PAGE_SIZE = 100


def _index_includes(includes: dict[str, list[dict]]) -> dict[str, dict[str, dict]]:
    """Flatten includes into {kind: {id_or_key: obj}} lookup tables."""
    return {
        "users": {u["id"]: u for u in includes.get("users", [])},
        "media": {m["media_key"]: m for m in includes.get("media", [])},
        "tweets": {t["id"]: t for t in includes.get("tweets", [])},
    }


def _attach_includes(tweet: dict[str, Any], lookup: dict[str, dict[str, dict]]) -> dict[str, Any]:
    """Inline author, media, and referenced tweets onto the tweet record."""
    out = dict(tweet)
    out["_author"] = lookup["users"].get(tweet.get("author_id"))
    media_keys = (tweet.get("attachments") or {}).get("media_keys") or []
    out["_media"] = [lookup["media"][k] for k in media_keys if k in lookup["media"]]
    refs = tweet.get("referenced_tweets") or []
    out["_referenced"] = [
        {**ref, "tweet": lookup["tweets"].get(ref["id"])} for ref in refs
    ]
    return out


def fetch_bookmarks(
    access_token: str,
    user_id: str,
    since_id: str | None = None,
) -> Iterator[dict[str, Any]]:
    """Yield bookmarks newest-first, stopping when since_id is reached or pages exhausted.

    Stops early if a yielded tweet's id == since_id (we've already processed it
    and everything older). The API caps total reachable bookmarks at 800.
    """
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {access_token}"})

    pagination_token: str | None = None
    while True:
        params: dict[str, str] = {
            "max_results": str(PAGE_SIZE),
            "tweet.fields": TWEET_FIELDS,
            "expansions": EXPANSIONS,
            "user.fields": USER_FIELDS,
            "media.fields": MEDIA_FIELDS,
        }
        if pagination_token:
            params["pagination_token"] = pagination_token

        resp = session.get(BOOKMARKS_URL.format(user_id=user_id), params=params, timeout=30)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", "60"))
            time.sleep(retry_after)
            continue
        if not resp.ok:
            raise RuntimeError(f"Bookmarks fetch failed ({resp.status_code}): {resp.text}")

        body = resp.json()
        tweets = body.get("data") or []
        lookup = _index_includes(body.get("includes") or {})

        for tweet in tweets:
            if since_id and tweet["id"] == since_id:
                return
            yield _attach_includes(tweet, lookup)

        meta = body.get("meta") or {}
        pagination_token = meta.get("next_token")
        if not pagination_token:
            return
