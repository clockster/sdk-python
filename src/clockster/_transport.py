"""Everything between a generated method and httpx.

One place decides how a query parameter is written, what a refusal becomes and where the token
goes, so the generated half is the operations and nothing else.
"""

from __future__ import annotations

from typing import IO, Any

import httpx

from .errors import STATUS_ERRORS, ClocksterError, ServerError

DEFAULT_BASE_URL = "https://api.clockster.com"

DEFAULT_TIMEOUT = 30.0


def _encode(query: dict[str, Any]) -> dict[str, str]:
    """Query parameters as this API reads them.

    A list travels comma-separated rather than as a repeated `field[]` — both are accepted, and
    this is the one the document describes. `None` is not a value: an omitted parameter and an
    empty one mean different things, and only the first is what a default argument means here.
    """
    out: dict[str, str] = {}

    for name, value in query.items():
        if value is None:
            continue

        if isinstance(value, bool):
            out[name] = "true" if value else "false"
        elif isinstance(value, list | tuple):
            if len(value) > 0:
                out[name] = ",".join(str(item) for item in value)
        else:
            out[name] = str(value)

    return out


class _Transport:
    """The half of a call that is the same on every operation."""

    def __init__(
        self,
        token: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        if not token:
            raise ValueError("A company API key is required. Create one under Settings, API.")

        self._token = token
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def _build(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None,
        json: Any,
        files: dict[str, tuple[str, bytes | IO[bytes]]] | None,
        data: dict[str, Any] | None,
        idempotency_key: str | None,
    ) -> dict[str, Any]:
        # Read per call rather than held in a header, so a rotated key does not need a new client.
        headers = {"Authorization": f"Bearer {self._token}", "Accept": "application/json"}

        if idempotency_key is not None:
            headers["Idempotency-Key"] = idempotency_key

        request: dict[str, Any] = {
            "method": method,
            "url": f"{self._base_url}{path}",
            "headers": headers,
            "params": _encode(query or {}),
        }

        if json is not None:
            request["json"] = json

        if files is not None:
            request["files"] = files
            # Multipart carries its other fields beside the bytes, and an omitted one is omitted.
            request["data"] = {k: v for k, v in (data or {}).items() if v is not None}

        return request

    def _answer(self, response: httpx.Response) -> Any:
        if response.is_success:
            # 204 has no body, and neither has a HEAD. Everything this API answers with is JSON.
            return None if not response.content else response.json()

        raise self._refusal(response)

    def _refusal(self, response: httpx.Response) -> ClocksterError:
        try:
            body = response.json()
        except ValueError:
            # An edge refusal can answer before the application does, and need not be JSON.
            body = None

        error = body.get("error", {}) if isinstance(body, dict) else {}
        status = response.status_code
        kind = STATUS_ERRORS.get(status, ServerError if status >= 500 else ClocksterError)
        extra: dict[str, Any] = {}

        if kind.__name__ == "RateLimitError":
            retry = response.headers.get("Retry-After")
            extra["retry_after"] = int(retry) if retry and retry.isdigit() else None

        return kind(
            error.get("message") or f"The API answered {status}.",
            status=status,
            code=error.get("code") or "unknown",
            request_id=error.get("request_id"),
            errors=error.get("errors"),
            body=body,
            **extra,
        )


class _SyncTransport(_Transport):
    def __init__(
        self,
        token: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        client: httpx.Client | None = None,
    ) -> None:
        super().__init__(token, base_url=base_url, timeout=timeout)
        # A client supplied here is the caller's to close; one made here is closed with the SDK.
        self._owned = client is None
        self._client = client or httpx.Client(timeout=timeout)

    def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        json: Any = None,
        files: dict[str, tuple[str, bytes | IO[bytes]]] | None = None,
        data: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        built = self._build(
            method,
            path,
            query=query,
            json=json,
            files=files,
            data=data,
            idempotency_key=idempotency_key,
        )

        return self._answer(self._client.request(**built))

    def close(self) -> None:
        if self._owned:
            self._client.close()


class _AsyncTransport(_Transport):
    def __init__(
        self,
        token: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(token, base_url=base_url, timeout=timeout)
        self._owned = client is None
        self._client = client or httpx.AsyncClient(timeout=timeout)

    async def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        json: Any = None,
        files: dict[str, tuple[str, bytes | IO[bytes]]] | None = None,
        data: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        built = self._build(
            method,
            path,
            query=query,
            json=json,
            files=files,
            data=data,
            idempotency_key=idempotency_key,
        )

        return self._answer(await self._client.request(**built))

    async def aclose(self) -> None:
        if self._owned:
            await self._client.aclose()


class _Namespace:
    """A group of operations, holding the transport they are called through."""

    def __init__(self, transport: _SyncTransport) -> None:
        self._transport = transport


class _AsyncNamespace:
    def __init__(self, transport: _AsyncTransport) -> None:
        self._transport = transport
