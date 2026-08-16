"""What the transport does with a call, against a stub rather than the API."""

from __future__ import annotations

import asyncio
import json
from typing import Any, cast

import httpx
import pytest

from clockster import (
    AsyncClockster,
    AuthenticationError,
    Clockster,
    ClocksterError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from clockster.models import SchedulesCreateBody, UsersUpsertBody


def stub(
    answer: dict[str, Any] | None = None,
    *,
    status: int = 200,
    headers: dict[str, str] | None = None,
    seen: list[httpx.Request] | None = None,
) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)

        return httpx.Response(status, json=answer if answer is not None else {}, headers=headers)

    return httpx.Client(transport=httpx.MockTransport(handler))


def client(**kwargs: Any) -> Clockster:
    return Clockster("token", client=stub(**kwargs))


def test_answers_the_parsed_body() -> None:
    # Compared as a plain dictionary: what comes back IS one, and the TypedDict is a description
    # of it rather than a thing this package built.
    answer: Any = client(answer={"data": [{"id": 1}]}).users.list()

    assert answer == {"data": [{"id": 1}]}


def test_carries_the_token_on_every_call() -> None:
    seen: list[httpx.Request] = []

    client(answer={"data": []}, seen=seen).users.list()

    assert seen[0].headers["Authorization"] == "Bearer token"
    assert seen[0].headers["Accept"] == "application/json"


def test_writes_a_list_parameter_comma_separated() -> None:
    seen: list[httpx.Request] = []

    client(answer={"data": []}, seen=seen).users.list(
        include=["location", "department"], ids=[1, 2]
    )

    # Both forms are accepted by the API; this is the one the document describes, and the one that
    # keeps the parameter called `include` rather than `include[]`.
    assert seen[0].url.params["include"] == "location,department"
    assert seen[0].url.params["ids"] == "1,2"


def test_leaves_out_what_was_not_asked_for() -> None:
    seen: list[httpx.Request] = []

    client(answer={"data": []}, seen=seen).users.list(per_page=50, search=None)

    # An omitted filter and an empty one mean different things, and a default argument is the first.
    assert dict(seen[0].url.params) == {"per_page": "50"}


def test_writes_a_boolean_as_the_api_reads_one() -> None:
    seen: list[httpx.Request] = []

    client(answer={"data": []}, seen=seen).webhooks.deliveries.list(pending=True, successful=False)

    assert seen[0].url.params["pending"] == "true"
    assert seen[0].url.params["successful"] == "false"


def test_puts_a_path_parameter_in_the_path() -> None:
    seen: list[httpx.Request] = []

    client(answer={"data": {"id": 7}}, seen=seen).users.get(7)

    assert seen[0].url.path == "/company/v3/users/7"


def test_sends_a_body_as_json() -> None:
    seen: list[httpx.Request] = []
    body: UsersUpsertBody = {
        "users": [
            {"external_id": "HR-1", "first_name": "Aisulu", "role": "employee", "location_id": 1}
        ]
    }

    client(answer={"data": []}, seen=seen).users.upsert(body)

    assert json.loads(seen[0].content) == body
    assert seen[0].headers["Content-Type"] == "application/json"


def test_carries_an_idempotency_key_where_the_operation_takes_one() -> None:
    seen: list[httpx.Request] = []

    empty: SchedulesCreateBody = {"schedules": []}

    client(answer={"data": []}, seen=seen).schedules.create(empty, idempotency_key="abc")

    assert seen[0].headers["Idempotency-Key"] == "abc"


def test_uploads_bytes_as_multipart() -> None:
    seen: list[httpx.Request] = []

    client(answer={"data": {"id": 1}}, seen=seen).files.upload(
        b"%PDF-1.4", filename="agreement.pdf"
    )

    assert seen[0].headers["Content-Type"].startswith("multipart/form-data")
    assert b"agreement.pdf" in seen[0].content


def test_raises_the_refusal_rather_than_answering_it() -> None:
    refusal = {"error": {"code": "not_found", "message": "No such row.", "request_id": "req-1"}}

    with pytest.raises(NotFoundError) as raised:
        client(answer=refusal, status=404).users.get(9)

    assert raised.value.code == "not_found"
    assert raised.value.request_id == "req-1"
    assert raised.value.status == 404
    assert isinstance(raised.value, ClocksterError)


def test_names_the_fields_a_validation_refusal_is_about() -> None:
    refusal = {
        "error": {
            "code": "validation_failed",
            "message": "The given data was invalid.",
            "request_id": "req-2",
            "errors": {"users.0.role": ["The role field is required."]},
        }
    }

    # A body the API will refuse, which is the point, so the type is not the one it wants.
    incomplete = cast(UsersUpsertBody, {"users": [{}]})

    with pytest.raises(ValidationError) as raised:
        client(answer=refusal, status=422).users.upsert(incomplete)

    assert raised.value.errors == {"users.0.role": ["The role field is required."]}


def test_reads_retry_after_off_a_rate_limit() -> None:
    refusal = {"error": {"code": "rate_limited", "message": "Too many.", "request_id": "req-3"}}

    with pytest.raises(RateLimitError) as raised:
        client(answer=refusal, status=429, headers={"Retry-After": "17"}).users.list()

    assert raised.value.retry_after == 17


def test_survives_a_refusal_that_is_not_ours() -> None:
    # An edge refusal can answer before the application does, and need not be JSON.
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, text="<html>gateway</html>")

    with pytest.raises(AuthenticationError) as raised:
        Clockster("token", client=httpx.Client(transport=httpx.MockTransport(handler))).users.list()

    assert raised.value.code == "unknown"
    assert raised.value.status == 401


def test_refuses_to_be_built_without_a_key() -> None:
    with pytest.raises(ValueError):
        Clockster("")


def test_the_async_client_answers_the_same_body() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": [{"id": 1}]})

    async def scenario() -> Any:
        # Run through asyncio directly rather than through a plugin: one test needs a loop, and a
        # dependency for it would be a dependency for everybody running the suite.
        async with AsyncClockster(
            "token", client=httpx.AsyncClient(transport=httpx.MockTransport(handler))
        ) as clockster:
            return await clockster.users.list()

    assert asyncio.run(scenario()) == {"data": [{"id": 1}]}
