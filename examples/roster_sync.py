"""Sync a roster from a CSV into Clockster, and dismiss whoever is no longer in it.

The shape a real HR integration has: your system knows people by a key of its own, and every sync
is "here is everybody, make it so". `external_id` is what makes that idempotent — send it on every
person and the second run updates rather than duplicates.

    export CLOCKSTER_TOKEN=...
    python examples/roster_sync.py people.csv

The file wants a header row:

    external_id,first_name,last_name,email,phone,location_code,location_title

Nothing is deleted. Somebody missing from the file is dismissed, which frees their seat and leaves
their attendance, payroll and documents readable — see the note on `users.dismiss` in the API
documentation for what dismissal does that cannot be undone.
"""

from __future__ import annotations

import csv
import os
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from clockster import DEFAULT_BASE_URL, Clockster, ValidationError, paginate
from clockster.models import LocationsUpsertItem, UsersDismissUser, UsersUpsertUser

# The roster endpoint takes 100 people a call, and says so; the rest is one round trip each.
BATCH = 100


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def chunks(people: list[UsersUpsertUser]) -> Iterator[list[UsersUpsertUser]]:
    for start in range(0, len(people), BATCH):
        yield people[start : start + BATCH]


def locations_by_code(clockster: Clockster, source: list[dict[str, str]]) -> dict[str, int]:
    """Write the locations the file names, and read their ids back out of the answer.

    An employee is filed against a location by id, and the file knows only its own code — so the
    codes go up as `external_id` and come back beside the id they were given.
    """
    named = {
        row["location_code"]: row["location_title"] for row in source if row.get("location_code")
    }

    if not named:
        return {}

    items: list[LocationsUpsertItem] = [
        {"external_id": code, "title": title} for code, title in sorted(named.items())
    ]

    answer = clockster.locations.upsert({"items": items})

    return {
        outcome["external_id"]: outcome["id"]
        for outcome in answer["data"]
        if outcome["external_id"]
    }


def person(row: dict[str, str], locations: dict[str, int]) -> UsersUpsertUser:
    person: UsersUpsertUser = {
        "external_id": row["external_id"],
        "first_name": row["first_name"],
        "role": "employee",
        "location_id": locations[row["location_code"]],
    }

    # Sent only where the file has something to say: an empty string is not an absent value, and
    # writing one would blank a field somebody filled in the web application.
    if row.get("last_name"):
        person["last_name"] = row["last_name"]

    if row.get("email"):
        person["email"] = row["email"]

    if row.get("phone"):
        person["phone"] = row["phone"]

    return person


def dismissed(clockster: Clockster, keys: set[str]) -> list[UsersDismissUser]:
    """Everyone on file here, not in the roster, and not already gone."""
    leaving: list[UsersDismissUser] = []

    for employee in paginate(clockster.users.list, per_page=BATCH, status="active"):
        external_id = employee["external_id"]

        if external_id and external_id not in keys:
            leaving.append({"external_id": external_id})

    return leaving


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} people.csv", file=sys.stderr)

        return 2

    token = os.environ.get("CLOCKSTER_TOKEN")

    if not token:
        print("Set CLOCKSTER_TOKEN to a company API key (Settings, API).", file=sys.stderr)

        return 2

    source = rows(Path(argv[1]))

    # A demo stand answers the same API; production is the default.
    base_url = os.environ.get("CLOCKSTER_BASE_URL") or DEFAULT_BASE_URL

    with Clockster(token, base_url=base_url) as clockster:
        company: Any = clockster.me()
        print(f"Syncing {len(source)} people into {company['data']['title']}.")

        locations = locations_by_code(clockster, source)
        people = [person(row, locations) for row in source]

        written = 0

        try:
            for batch in chunks(people):
                answer = clockster.users.upsert({"users": batch})
                written += len(answer["data"])
                print(f"  {written}/{len(people)}")
        except ValidationError as refusal:
            # None of the batch landed: the write is all or nothing, so the file is fixable and
            # the whole run can be repeated.
            print(f"Refused: {refusal.code} {refusal.errors}", file=sys.stderr)

            return 1

        leaving = dismissed(clockster, {row["external_id"] for row in source})

        if leaving:
            clockster.users.dismiss({"users": leaving})

        print(f"{written} written, {len(leaving)} dismissed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
