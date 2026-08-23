"""The closed sets of values, as the document names them."""

from __future__ import annotations

from typing import get_args

from clockster.models import (
    DepartmentsInclude,
    LocationsInclude,
    TasksPriority,
    UsersRole,
    UsersStatus,
    WebhooksEvent,
)


def test_a_set_is_the_values_it_holds() -> None:
    # An alias rather than constants: the values are the type, so a checker completes against them
    # and nothing has to be unwrapped to send one.
    assert get_args(UsersRole) == ("admin", "employee")
    assert get_args(UsersStatus) == ("active", "dismissed", "all")


def test_a_set_of_numbers_is_named_too() -> None:
    # Where the other clients write `0|1` out, a Literal names it as readily as it names words.
    assert get_args(TasksPriority) == (0, 1)


def test_one_resource_inside_another_shares_the_set() -> None:
    # `webhooks` and `webhooks/deliveries` name the same events, and the document says so once.
    assert "task.approved" in get_args(WebhooksEvent)


def test_unrelated_resources_keep_their_own_name() -> None:
    # Two sets that read alike today and are not promised to move together, so the document names
    # them separately and a caller writes whichever belongs to the call being made.
    assert get_args(LocationsInclude) == ("managers",)
    assert get_args(DepartmentsInclude) == ("managers",)

    # Two names for one type here, and only that: `typing` hands back the same object for two
    # identical Literals, so Python cannot tell them apart at run time even though the document
    # can. The names are what the reader and the checker have, which is what they are for.
    assert LocationsInclude is DepartmentsInclude
