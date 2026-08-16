"""Official Python SDK for the Clockster Company API.

    from clockster import Clockster

    clockster = Clockster(token=os.environ["CLOCKSTER_TOKEN"])
    users = clockster.users.list(per_page=100, include=["location"])

Typed from https://api.clockster.com/openapi/v3.json. The answer is the parsed body, nothing is
validated on the way in, and a refusal is raised as a `ClocksterError`.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from ._client import AsyncClockster, Clockster
from ._transport import DEFAULT_BASE_URL
from .errors import (
    AuthenticationError,
    ClocksterError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .pagination import paginate, paginate_async
from .webhooks import WebhookVerificationError, verify_webhook

__all__ = [
    "DEFAULT_BASE_URL",
    "AsyncClockster",
    "AuthenticationError",
    "Clockster",
    "ClocksterError",
    "ConflictError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    "WebhookVerificationError",
    "paginate",
    "paginate_async",
    "verify_webhook",
]

try:
    __version__ = version("clockster")
except PackageNotFoundError:  # pragma: no cover - a source tree nobody installed
    __version__ = "0.0.0"
