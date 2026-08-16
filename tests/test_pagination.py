"""Walking a listing, against a stub listing rather than the API."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from clockster import paginate, paginate_async


def listing(pages: list[list[str]], asked: list[str | None] | None = None) -> Any:
    """A listing of `pages` pages, recording the cursor it was asked for each time."""

    def page(*, cursor: str | None = None, **filters: Any) -> dict[str, Any]:
        if asked is not None:
            asked.append(cursor)

        index = 0 if cursor is None else int(cursor)
        following = str(index + 1) if index + 1 < len(pages) else None

        return {"data": pages[index], "meta": {"next_cursor": following}}

    return page


def test_yields_every_row_across_every_page() -> None:
    assert list(paginate(listing([["a", "b"], ["c"], ["d", "e"]]))) == ["a", "b", "c", "d", "e"]


def test_asks_for_the_first_page_without_a_cursor_then_the_one_it_was_given() -> None:
    asked: list[str | None] = []

    list(paginate(listing([["a"], ["b"], ["c"]], asked)))

    assert asked == [None, "1", "2"]


def test_passes_the_filters_through_unchanged() -> None:
    seen: list[dict[str, Any]] = []

    def page(*, cursor: str | None = None, **filters: Any) -> dict[str, Any]:
        seen.append(filters)

        return {"data": ["a"], "meta": {"next_cursor": None}}

    list(paginate(page, per_page=100, include=["location"]))

    assert seen == [{"per_page": 100, "include": ["location"]}]


def test_stops_on_a_single_page() -> None:
    asked: list[str | None] = []

    assert list(paginate(listing([["a"]], asked))) == ["a"]
    assert asked == [None]


def test_yields_nothing_for_an_empty_listing() -> None:
    assert list(paginate(listing([[]]))) == []


def test_raises_the_refusal_rather_than_ending_the_listing_quietly() -> None:
    def refused(*, cursor: str | None = None, **filters: Any) -> dict[str, Any]:
        raise RuntimeError("rate limited")

    with pytest.raises(RuntimeError):
        list(paginate(refused))


def test_refuses_in_the_middle_after_the_rows_it_did_read() -> None:
    calls = 0

    def halfway(*, cursor: str | None = None, **filters: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1

        if calls == 1:
            return {"data": ["a"], "meta": {"next_cursor": "1"}}

        raise RuntimeError("gone")

    rows: list[str] = []

    with pytest.raises(RuntimeError):
        for row in paginate(halfway):
            rows.append(row)

    assert rows == ["a"]


def test_stops_when_a_cursor_repeats() -> None:
    calls = 0

    def stuck(*, cursor: str | None = None, **filters: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1

        return {"data": ["a"], "meta": {"next_cursor": "same"}}

    # A server handing back the same cursor would otherwise loop until the process is killed.
    assert list(paginate(stuck)) == ["a", "a"]
    assert calls == 2


def test_the_async_walk_yields_the_same_rows() -> None:
    pages = [["a", "b"], ["c"]]

    async def page(*, cursor: str | None = None, **filters: Any) -> dict[str, Any]:
        index = 0 if cursor is None else int(cursor)
        following = str(index + 1) if index + 1 < len(pages) else None

        return {"data": pages[index], "meta": {"next_cursor": following}}

    async def collect() -> list[str]:
        return [row async for row in paginate_async(page)]

    assert asyncio.run(collect()) == ["a", "b", "c"]
