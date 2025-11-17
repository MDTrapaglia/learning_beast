"""Security utilities to keep inputs and sessions safe."""
from __future__ import annotations

import html
import re
import secrets
import string
from datetime import datetime, timedelta
from typing import Dict

from fastapi import HTTPException, status

SAFE_TEXT_PATTERN = re.compile(r"[^a-zA-Z0-9 .,;:?!¡¿'\"\-\n]")
MAX_TEXT_LENGTH = 600
SESSION_TOKEN_LENGTH = 32
ALLOWED_SESSION_CHARS = string.ascii_letters + string.digits


def sanitize_free_text(raw_text: str) -> str:
    """Return a sanitized text that is safe to store and display."""

    if not isinstance(raw_text, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid text payload provided.",
        )

    trimmed = raw_text.strip()[:MAX_TEXT_LENGTH]
    cleaned = SAFE_TEXT_PATTERN.sub("", trimmed)
    escaped = html.escape(cleaned)
    return escaped


def generate_session_token() -> str:
    """Create a cryptographically secure token for user sessions."""

    return "".join(secrets.choice(ALLOWED_SESSION_CHARS) for _ in range(SESSION_TOKEN_LENGTH))


def ensure_session_is_active(expires_at: datetime) -> None:
    """Raise when the session already expired."""

    if datetime.utcnow() > expires_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please start a new learning path.",
        )


def compute_expiration(minutes: int) -> datetime:
    """Return expiration time based on current UTC time."""

    return datetime.utcnow() + timedelta(minutes=minutes)


def safe_numeric_weight(value: float) -> float:
    """Clamp numeric weights to avoid NaNs or injection via JSON payloads."""

    if not isinstance(value, (int, float)):
        raise HTTPException(status_code=400, detail="Invalid numeric weight.")
    return max(-1.0, min(1.0, float(value)))


def normalized_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """Return sanitized weights dictionary."""

    return {key: safe_numeric_weight(val) for key, val in weights.items()}
