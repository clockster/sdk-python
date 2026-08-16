# clockster

Official Python SDK for the [Clockster Company API](https://api.clockster.com/openapi/v3.json).

Server-to-server client for a company's employees, structure, schedules, attendance, tasks and
documents. Typed from the API's OpenAPI document. One dependency, `httpx`.

```bash
pip install clockster
```

Requires Python 3.10 or newer.

## Quickstart

One token authenticates one company. Create it under Settings → API in the web application.

```python
import os

from clockster import Clockster

clockster = Clockster(token=os.environ["CLOCKSTER_TOKEN"])

me = clockster.me()

locations = clockster.locations.upsert({"items": [{"external_id": "HQ", "title": "Head office"}]})

clockster.users.upsert(
    {
        "users": [
            {
                "external_id": "HR-1",
                "first_name": "Aisulu",
                "role": "employee",
                "location_id": locations["data"][0]["id"],
            }
        ]
    }
)

timesheets = clockster.timesheets.list(date_from="2026-08-01", date_to="2026-08-31")
```

A method answers the parsed body, so rows are `response["data"]`. Nothing is validated on the way
in: the answer is the JSON as it arrived, and a field we add tomorrow reaches your code today.

## Options

```python
clockster = Clockster(
    token,
    base_url="https://demo.clockster.com",  # a demo stand instead of production
    timeout=60.0,                           # seconds, applied to each request
    user_agent="acme-hr/1.4",               # names your integration in our request log
    client=recording,                       # your own httpx client, yours to close
)
```

Requests carry `clockster-python/<version>` unless `user_agent` says otherwise, so our request log
shows which client made a call. The token is read per request, so rotating it does not require a
new client.

## Refusals

A refusal is raised, never returned.

```python
from clockster import ClocksterError, RateLimitError, ValidationError

try:
    clockster.users.upsert({"users": [{"first_name": "Aisulu"}]})
except ValidationError as error:
    print(error.code, error.errors)  # validation_failed {'users.0.role': [...]}
except RateLimitError as error:
    print(error.retry_after)  # seconds, from Retry-After
except ClocksterError as error:
    print(error.code, error.request_id)
```

`code` is what to branch on; `message` is for a log; quote `request_id` when asking us about a
call. `AuthenticationError`, `ForbiddenError`, `NotFoundError`, `ConflictError`, `ValidationError`,
`RateLimitError` and `ServerError` all descend from `ClocksterError`, so catching that one catches
everything.

## What is available

| Group | Operations |
| --- | --- |
| `me()` | — |
| `users` | `list` `get` `upsert` `dismiss` |
| `locations`, `departments`, `positions`, `user_filters` | `list` `get` `upsert` `delete` |
| `schedules` | `create` `get` `delete` |
| `attendance` | `list` `record` |
| `timesheets` | `list` |
| `tasks` | `list` `get` `upsert` |
| `documents` | `list` `get` `upsert` `delete` |
| `files` | `upload` |
| `payroll.payslips` | `list` |
| `user_requests` | `list` `get` |
| `webhooks` | `list` `get` `create` `update` `delete` `rotate_secret` |
| `webhooks.deliveries` | `list` `get` `redeliver` |
| `webhooks.events` | `list` |

## Paging

Listings are cursor-paged. `paginate` walks the pages and yields the rows:

```python
from clockster import paginate

for user in paginate(clockster.users.list, per_page=100):
    print(user["external_id"] or user["id"])
```

Filters go where you would put them anyway; the cursor is the helper's business:

```python
for mark in paginate(clockster.attendance.list, date_from="2026-08-01", date_to="2026-08-31"):
    print(mark["id"])
```

A refused page raises where it was refused — a half-read listing is not a result. A cursor is bound
to the filters it was issued under; change them and start again.

Listings answer oldest first, so a first call on a long-lived company lands years back. Ask with
`updated_since` when you want recent activity rather than all of it.

## Relations

A related object is absent unless `include` names it, and its type says so: `location` on an
employee, `user` on a mark.

```python
users = clockster.users.list(include=["location", "department"])

print(users["data"][0]["location"]["title"])
```

Every list parameter takes a list and travels comma-separated: `include`, `ids`, `locations` and
the rest.

An absent key is not the same as a null one. `null` means we know the value is empty; absent means
you did not ask.

## Types

The shapes are `TypedDict`s, so a type checker sees the fields of a row while your code keeps
plain dictionaries:

```python
from clockster.models import UsersListRow

user: UsersListRow
for user in paginate(clockster.users.list):
    print(user["first_name"])
```

## Async

`AsyncClockster` mirrors the whole surface.

```python
from clockster import AsyncClockster, paginate_async

async with AsyncClockster(token=os.environ["CLOCKSTER_TOKEN"]) as clockster:
    timesheets = await clockster.timesheets.list(date_from="2026-08-01", date_to="2026-08-31")

    async for user in paginate_async(clockster.users.list, per_page=100):
        print(user["id"])
```

## Webhooks

`verify_webhook` takes the body as received and answers the event, so the only path to the event
runs through the check.

```python
from clockster import WebhookVerificationError, verify_webhook


@app.post("/clockster")
async def receive(request: Request) -> Response:
    try:
        event = verify_webhook(
            body=await request.body(),
            signature=request.headers.get("X-Clockster-Signature"),
            timestamp=request.headers.get("X-Clockster-Timestamp"),
            secret=os.environ["CLOCKSTER_WEBHOOK_SECRET"],
        )
    except WebhookVerificationError:
        return Response(status_code=400)

    queue.put(event)

    return Response(status_code=202)
```

- Pass the **raw bytes**. Re-serialising a parsed object does not reproduce what was signed.
- Answer **2xx quickly** and do the work afterwards; a timeout is retried.
- Deduplicate on **`id`**. The same event may arrive twice.

Deliveries older than five minutes are refused as replays; `tolerance_seconds` changes that.

## Versioning

Semver, independent of the API version. This package targets Company API v3; a new API version is a
major release here, not a second package.

## Examples

Two integrations of the shape most of them have, in [examples](examples): `roster_sync.py` writes a
roster in from a CSV and dismisses whoever is no longer in it, `timesheet_export.py` reads a month
out as CSV. Both are single files that use the package as published.

## Development

`src/clockster/_generated` is produced from `openapi/company-v3.json` and committed, so an API
change appears in review as the lines of the client it moves.

```bash
make spec        # refresh the specification from the deployed API
make generate    # regenerate the client from it
make check       # ruff, mypy and the tests
```

CI checks that the committed client is what the committed specification produces, and that every
operation is reachable on it. Drift against the deployed API is checked nightly.

## Licence

MIT. See [LICENSE](LICENSE).
