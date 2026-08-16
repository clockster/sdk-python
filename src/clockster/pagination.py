"""Walking a cursor-paged listing.

Thirteen of them page this way, and the loop is the same each time.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from typing import Any


def paginate(listing: Callable[..., Any], **filters: Any) -> Iterator[Any]:
    """Every row of a listing, one page at a time.

    Takes the method and the filters rather than a page: the cursor is this function's business,
    and everything else is the caller's.

        for user in paginate(clockster.users.list, per_page=100):
            print(user["external_id"] or user["id"])

    A refused page raises where it was refused, so a half-read listing is never mistaken for the
    whole of one. Annotate the loop variable to get the row type back:

        user: UsersListRow
        for user in paginate(clockster.users.list):
            ...

    A cursor is bound to the filters it was issued under; change them and start again.
    """
    cursor: str | None = None
    seen: set[str] = set()

    while True:
        page = listing(cursor=cursor, **filters)

        yield from page["data"]

        cursor = page.get("meta", {}).get("next_cursor")

        if cursor is None:
            return

        # A cursor that repeats would loop until the process is killed, which is worse than
        # stopping.
        if cursor in seen:
            return

        seen.add(cursor)


async def paginate_async(
    listing: Callable[..., Awaitable[Any]], **filters: Any
) -> AsyncIterator[Any]:
    """`paginate`, awaited.

    async for mark in paginate_async(clockster.attendance.list, date_from=..., date_to=...):
        ...
    """
    cursor: str | None = None
    seen: set[str] = set()

    while True:
        page = await listing(cursor=cursor, **filters)

        for row in page["data"]:
            yield row

        cursor = page.get("meta", {}).get("next_cursor")

        if cursor is None:
            return

        if cursor in seen:
            return

        seen.add(cursor)
