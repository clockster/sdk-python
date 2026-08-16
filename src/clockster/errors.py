"""What a refusal is raised as.

The API answers every refusal with one envelope — a code to branch on, a message for a log, and a
request id to quote when asking us about a call — so there is one exception carrying all three and a
subclass per status worth catching on its own.
"""

from __future__ import annotations

from typing import Any


class ClocksterError(Exception):
    """A call the API refused.

    `code` is what to branch on: it names the reason and does not change, where `message` is prose
    and may. `request_id` identifies this exact call in our logs.
    """

    def __init__(
        self,
        message: str,
        *,
        status: int,
        code: str,
        request_id: str | None = None,
        errors: dict[str, list[str]] | None = None,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.request_id = request_id
        # Named fields, on a refusal that names any.
        self.errors = errors or {}
        # The body as it arrived, for a refusal this package does not know the shape of.
        self.body = body

    def __str__(self) -> str:
        stamped = f" (request_id {self.request_id})" if self.request_id else ""

        return f"[{self.status} {self.code}] {self.message}{stamped}"


class AuthenticationError(ClocksterError):
    """401 — no token, or one this surface does not accept."""


class ForbiddenError(ClocksterError):
    """403 — a token without the ability this call needs."""


class NotFoundError(ClocksterError):
    """404 — no such row in the calling company. Another company's id answers this, not a 403."""


class ConflictError(ClocksterError):
    """409 — the row is there and cannot be changed the way you asked."""


class ValidationError(ClocksterError):
    """422 — the request was understood and refused. `errors` names the fields."""


class RateLimitError(ClocksterError):
    """429 — over the limit. `retry_after` is the seconds to wait, when the response said."""

    def __init__(self, *args: Any, retry_after: int | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.retry_after = retry_after


class ServerError(ClocksterError):
    """5xx — ours to fix. Retrying is safe on a read and on anything carrying an idempotency key."""


STATUS_ERRORS: dict[int, type[ClocksterError]] = {
    401: AuthenticationError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    422: ValidationError,
    429: RateLimitError,
}
