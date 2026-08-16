"""The signing check, against deliveries signed the way the backend signs them."""

from __future__ import annotations

import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest

from clockster import WebhookVerificationError, verify_webhook

SECRET = "0" * 64


def sign(body: str, timestamp: str, secret: str = SECRET) -> str:
    """Mirrors WebhookEnvelopeService::headers(): sha256= over `<timestamp>.<body>`."""
    digest = hmac.new(secret.encode(), f"{timestamp}.{body}".encode(), hashlib.sha256).hexdigest()

    return f"sha256={digest}"


def delivery(
    *, body: str | None = None, timestamp: str | None = None, secret: str = SECRET
) -> dict[str, Any]:
    when = timestamp or datetime.now(timezone.utc).isoformat()
    payload = body or json.dumps(
        {"id": 1, "event": "task.completed", "occurred_at": when, "data": {}}
    )

    return {
        "body": payload,
        "timestamp": when,
        "signature": sign(payload, when, secret),
        "secret": SECRET,
    }


def test_answers_the_event_of_a_genuine_delivery() -> None:
    event = verify_webhook(**delivery())

    assert event["event"] == "task.completed"
    assert event["id"] == 1


def test_accepts_the_raw_body_as_bytes() -> None:
    sent = delivery()
    sent["body"] = sent["body"].encode()

    assert verify_webhook(**sent)["event"] == "task.completed"


def test_refuses_a_body_altered_after_signing() -> None:
    sent = delivery()
    sent["body"] = sent["body"].replace("task.completed", "task.approved")

    with pytest.raises(WebhookVerificationError) as raised:
        verify_webhook(**sent)

    assert raised.value.reason == "signature_mismatch"


def test_refuses_a_signature_made_with_another_secret() -> None:
    with pytest.raises(WebhookVerificationError) as raised:
        verify_webhook(**delivery(secret="f" * 64))

    assert raised.value.reason == "signature_mismatch"


def test_refuses_a_body_reserialised_from_the_parsed_object() -> None:
    # Re-serialising a parsed body is the mistake this package exists to prevent.
    sent = delivery(body='{"id":1,  "event":"task.completed","occurred_at":"x","data":{}}')
    sent["body"] = json.dumps(json.loads(sent["body"]))

    with pytest.raises(WebhookVerificationError) as raised:
        verify_webhook(**sent)

    assert raised.value.reason == "signature_mismatch"


def test_refuses_a_delivery_older_than_the_tolerance() -> None:
    old = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()

    with pytest.raises(WebhookVerificationError) as raised:
        verify_webhook(**delivery(timestamp=old))

    assert raised.value.reason == "timestamp_outside_tolerance"


def test_accepts_an_old_delivery_where_the_tolerance_is_off() -> None:
    old = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

    assert (
        verify_webhook(**delivery(timestamp=old), tolerance_seconds=0)["event"] == "task.completed"
    )


def test_refuses_a_delivery_dated_in_the_future() -> None:
    # Absolute, so a receiver whose clock runs behind refuses rather than accepts indefinitely.
    ahead = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()

    with pytest.raises(WebhookVerificationError) as raised:
        verify_webhook(**delivery(timestamp=ahead))

    assert raised.value.reason == "timestamp_outside_tolerance"


def test_refuses_a_timestamp_that_is_not_an_instant() -> None:
    sent = delivery(timestamp="yesterday")

    with pytest.raises(WebhookVerificationError) as raised:
        verify_webhook(**sent)

    assert raised.value.reason == "timestamp_unreadable"


def test_refuses_a_delivery_without_a_signature() -> None:
    sent = delivery()
    sent["signature"] = None

    with pytest.raises(WebhookVerificationError) as raised:
        verify_webhook(**sent)

    assert raised.value.reason == "missing_signature"


def test_refuses_a_delivery_without_a_timestamp() -> None:
    sent = delivery()
    sent["timestamp"] = None

    with pytest.raises(WebhookVerificationError) as raised:
        verify_webhook(**sent)

    assert raised.value.reason == "missing_timestamp"


def test_refuses_a_signature_in_a_scheme_it_does_not_know() -> None:
    sent = delivery()
    sent["signature"] = sent["signature"].replace("sha256=", "md5=")

    with pytest.raises(WebhookVerificationError) as raised:
        verify_webhook(**sent)

    assert raised.value.reason == "unknown_scheme"


def test_refuses_a_body_that_is_signed_and_is_not_json() -> None:
    with pytest.raises(WebhookVerificationError) as raised:
        verify_webhook(**delivery(body="not json"))

    assert raised.value.reason == "body_unparseable"


def test_answers_a_trial_delivery_which_stands_for_no_recorded_event() -> None:
    when = datetime.now(timezone.utc).isoformat()
    body = json.dumps({"id": None, "event": "task.completed", "occurred_at": when, "data": {}})

    assert verify_webhook(**delivery(body=body, timestamp=when))["id"] is None
