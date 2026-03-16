from __future__ import annotations

import json
import logging
import os
import time
import urllib.request
from pathlib import Path

import jwt
from dotenv import load_dotenv
from fastapi import Header, HTTPException

_JWKS_CACHE: dict | None = None
_JWKS_CACHE_AT: float | None = None

load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)

logger = logging.getLogger("auth")


def _log_token_debug(token: str, reason: str) -> None:
    try:
        header = jwt.get_unverified_header(token)
    except Exception:
        header = {}

    try:
        payload = jwt.decode(token, options={"verify_signature": False})
    except Exception:
        payload = {}

    logger.warning(
        "Invalid token (%s). alg=%s kid=%s iss=%s aud=%s sub=%s exp=%s iat=%s",
        reason,
        header.get("alg"),
        header.get("kid"),
        payload.get("iss"),
        payload.get("aud"),
        payload.get("sub"),
        payload.get("exp"),
        payload.get("iat"),
    )


def _get_jwks() -> dict:
    global _JWKS_CACHE, _JWKS_CACHE_AT

    if _JWKS_CACHE and _JWKS_CACHE_AT and (time.time() - _JWKS_CACHE_AT) < 3600:
        return _JWKS_CACHE

    supabase_url = os.getenv("SUPABASE_URL")
    if not supabase_url:
        raise HTTPException(status_code=500, detail="Server auth misconfigured")

    jwks_url = f"{supabase_url.rstrip('/')}/auth/v1/keys"
    try:
        with urllib.request.urlopen(jwks_url, timeout=5) as response:
            payload = response.read().decode("utf-8")
            jwks = json.loads(payload)
    except Exception:
        raise HTTPException(status_code=503, detail="Unable to fetch JWKS")

    _JWKS_CACHE = jwks
    _JWKS_CACHE_AT = time.time()
    return jwks


def _decode_token(token: str) -> dict:
    try:
        header = jwt.get_unverified_header(token)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    alg = header.get("alg")
    if alg in {"RS256", "ES256"}:
        jwks = _get_jwks()
        kid = header.get("kid")
        keys = jwks.get("keys", [])
        key = next((item for item in keys if item.get("kid") == kid), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token")
        if alg == "RS256":
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
        else:
            public_key = jwt.algorithms.ECAlgorithm.from_jwk(json.dumps(key))
        return jwt.decode(token, public_key, algorithms=[alg], options={"verify_aud": False})

    secret = os.getenv("SUPABASE_JWT_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="Server auth misconfigured")
    return jwt.decode(token, secret, algorithms=["HS256"], options={"verify_aud": False})


def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = _decode_token(token)
    except HTTPException as exc:
        if exc.status_code == 503:
            raise
        _log_token_debug(token, f"http_{exc.status_code}")
        raise
    except jwt.PyJWTError:
        _log_token_debug(token, "jwt_error")
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return {"user_id": user_id, "email": payload.get("email")}
