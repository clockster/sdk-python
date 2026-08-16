"""Verifying a delivery, and reading the event out of it.

The check is the only path to the event: `verify_webhook` takes the body as it arrived and answers
the parsed event, so there is no way to act on one that was not verified.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Any, Literal

SCHEME = "sha256="

DEFAULT_TOLERANCE_SECONDS = 300

WebhookFailure = Literal[
    "missing_signature",
    "missing_timestamp",
    "unknown_scheme",
    "signature_mismatch",
    "timestamp_unreadable",
    "timestamp_outside_tolerance",
    "body_unparseable",
]


class WebhookVerificationError(Exception):
    """Raised for anything that would make a delivery unsafe to act on."""

    def __init__(self, message: str, reason: WebhookFailure) -> None:
        super().__init__(message)
        self.reason = reason


def verify_webhook(
    *,
    body: bytes | str,
    signature: str | None,
    timestamp: str | None,
    secret: str,
    tolerance_seconds: int = DEFAULT_TOLERANCE_SECONDS,
) -> dict[str, Any]:
    """Verify a delivery and answer the event it carries.

    :param body: the body as received. Re-serialising a parsed object does not reproduce the
        signed bytes, and the check will fail — read the raw request body.
    :param signature: the `X-Clockster-Signature` header.
    :param timestamp: the `X-Clockster-Timestamp` header, an ISO 8601 instant rather than a
        Unix time.
    :param secret: the signing secret of the endpoint.
    :param tolerance_seconds: maximum age; 0 accepts any. Refusing an old delivery is what stops a
        replay.

    :raises WebhookVerificationError: when the delivery is not provably ours, or is too old.

    The event carries `id` (null on a trial delivery, which stands for no recorded event), `event`,
    `occurred_at` and `data`. Answer 2xx quickly and do the work afterwards — a timeout is retried —
    and deduplicate on `id`, since the same event may arrive twice.
    """
    if not signature:
        raise WebhookVerificationError("No X-Clockster-Signature header.", "missing_signature")

    if not timestamp:
        raise WebhookVerificationError("No X-Clockster-Timestamp header.", "missing_timestamp")

    if not signature.startswith(SCHEME):
        raise WebhookVerificationError(f"Signature is not {SCHEME}<hex>.", "unknown_scheme")

    payload = body.encode("utf-8") if isinstance(body, str) else bytes(body)

    # The timestamp is inside what is signed, so it cannot be edited to widen the check below.
    expected = hmac.new(
        secret.encode("utf-8"), f"{timestamp}.".encode() + payload, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature[len(SCHEME) :], expected):
        raise WebhookVerificationError(
            "Signature does not match the body. Verify the bytes as received, before parsing them.",
            "signature_mismatch",
        )

    _assert_fresh(timestamp, tolerance_seconds)

    try:
        event: dict[str, Any] = json.loads(payload)
    except ValueError as error:
        raise WebhookVerificationError(
            "Body is signed but is not JSON.", "body_unparseable"
        ) from error

    return event


def _assert_fresh(timestamp: str, tolerance_seconds: int) -> None:
    if tolerance_seconds <= 0:
        return

    try:
        sent = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as error:
        raise WebhookVerificationError(
            f"Timestamp {timestamp} is not an ISO 8601 instant.", "timestamp_unreadable"
        ) from error

    if sent.tzinfo is None:
        sent = sent.replace(tzinfo=timezone.utc)

    # Absolute, so a receiver whose clock runs behind refuses rather than accepts indefinitely.
    if abs((datetime.now(timezone.utc) - sent).total_seconds()) > tolerance_seconds:
        raise WebhookVerificationError(
            f"Delivery is outside the {tolerance_seconds}s tolerance.",
            "timestamp_outside_tolerance",
        )
