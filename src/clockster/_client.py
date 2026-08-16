"""The client a caller constructs. Everything below the constructor is generated."""

from __future__ import annotations

from types import TracebackType

import httpx

from ._generated.api import _AsyncClocksterApi, _ClocksterApi
from ._transport import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, _AsyncTransport, _SyncTransport


class Clockster(_ClocksterApi):
    """The Company API, one token to one company.

    The key is issued in the web application, under Settings, API.

        clockster = Clockster(token=os.environ["CLOCKSTER_TOKEN"])
        me = clockster.me()
        users = clockster.users.list(per_page=100, include=["location"])

    Every method answers the parsed body — `users["data"]` is the rows — and raises
    `ClocksterError` on a refusal. Deliveries are verified with `verify_webhook`.
    """

    def __init__(
        self,
        token: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        client: httpx.Client | None = None,
    ) -> None:
        """
        :param token: the company API key.
        :param base_url: point at a demo stand instead of production.
        :param timeout: seconds, applied to each request.
        :param client: your own httpx client — a proxy, a retrying transport, a recording one.
            Supplying one leaves closing it to you.
        """
        self._sync_transport = _SyncTransport(
            token, base_url=base_url, timeout=timeout, client=client
        )

        super().__init__(self._sync_transport)

    def close(self) -> None:
        """Close the connection pool, unless the httpx client came from outside."""
        self._sync_transport.close()

    def __enter__(self) -> Clockster:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()


class AsyncClockster(_AsyncClocksterApi):
    """The same API, awaited.

    async with AsyncClockster(token=...) as clockster:
        users = await clockster.users.list(per_page=100)
    """

    def __init__(
        self,
        token: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._async_transport = _AsyncTransport(
            token, base_url=base_url, timeout=timeout, client=client
        )

        super().__init__(self._async_transport)

    async def aclose(self) -> None:
        await self._async_transport.aclose()

    async def __aenter__(self) -> AsyncClockster:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()
