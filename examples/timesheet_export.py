"""Export a month of timesheets to CSV: one row per person per day.

    export CLOCKSTER_TOKEN=...
    python examples/timesheet_export.py 2026-08 > august.csv

The window is required and capped at a month, which is why this takes one. Every day of it gets a
row, including the ones nobody was scheduled for — `planned` is null there, and that is a day off
rather than a missing row.

Times are seconds on the wire. They are written as hours here because that is what a spreadsheet
wants, and the conversion is the only arithmetic this file does: `time_worked` is not `out` minus
`in`, since grace windows and the break are already accounted for by the API.
"""

from __future__ import annotations

import calendar
import csv
import os
import sys
from datetime import date

from clockster import DEFAULT_BASE_URL, Clockster, paginate
from clockster.models import TimesheetsListRow

COLUMNS = [
    "date",
    "employee",
    "external_id",
    "kind",
    "planned_hours",
    "worked_hours",
    "late_minutes",
    "early_left_minutes",
    "overworked_hours",
]


def window(month: str) -> tuple[str, str]:
    """The first and last day of `YYYY-MM`."""
    year, index = (int(part) for part in month.split("-", 1))
    last = calendar.monthrange(year, index)[1]

    return date(year, index, 1).isoformat(), date(year, index, last).isoformat()


def hours(seconds: int) -> str:
    return f"{seconds / 3600:.2f}"


def minutes(seconds: int) -> str:
    return f"{seconds / 60:.0f}"


def name(row: TimesheetsListRow) -> str:
    employee = row["user"]
    parts = [employee.get("last_name") or "", employee.get("first_name") or ""]

    return " ".join(part for part in parts if part) or f"#{employee['id']}"


def line(row: TimesheetsListRow) -> list[str]:
    planned = row["planned"]
    actual = row.get("actual")
    variance = row.get("variance")

    # A day nobody was scheduled for. Not a gap in the data — the plan is what is absent, and the
    # hours worked on it, if any, are still reported.
    kind = "day off" if planned is None else (planned["leave_type"] or planned["type"])

    return [
        row["date"],
        name(row),
        row["user"]["external_id"] or "",
        kind,
        hours(planned["time_planned"]) if planned else "",
        hours(actual["time_worked"]) if actual else "",
        minutes(variance["time_late"]) if variance else "",
        minutes(variance["time_early_left"]) if variance else "",
        hours(variance["time_overworked"]) if variance else "",
    ]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} YYYY-MM", file=sys.stderr)

        return 2

    token = os.environ.get("CLOCKSTER_TOKEN")

    if not token:
        print("Set CLOCKSTER_TOKEN to a company API key (Settings, API).", file=sys.stderr)

        return 2

    date_from, date_to = window(argv[1])
    out = csv.writer(sys.stdout)
    out.writerow(COLUMNS)

    # A demo stand answers the same API; production is the default.
    base_url = os.environ.get("CLOCKSTER_BASE_URL") or DEFAULT_BASE_URL

    with Clockster(token, base_url=base_url) as clockster:
        row: TimesheetsListRow

        # Paging walks people rather than rows, so one person's whole month arrives together and a
        # monthly total never has to be assembled across two pages. `include` is what makes the
        # call expensive: ask for the facts only because this export prints them.
        for row in paginate(
            clockster.timesheets.list,
            date_from=date_from,
            date_to=date_to,
            include=["actual", "variance", "user"],
        ):
            out.writerow(line(row))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
