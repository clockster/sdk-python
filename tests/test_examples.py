"""The examples, exercised where they can be: the parts that do not need the API.

They are documentation, and documentation that stopped compiling against the client is worse than
none — this file is what notices.
"""

from __future__ import annotations

import roster_sync
import timesheet_export
from clockster.models import TimesheetsListRow, UsersUpsertUser


def test_the_window_is_the_whole_month() -> None:
    assert timesheet_export.window("2026-08") == ("2026-08-01", "2026-08-31")
    # February, and the leap year that makes reading a calendar worth it.
    assert timesheet_export.window("2024-02") == ("2024-02-01", "2024-02-29")


def test_a_worked_day_is_written_in_hours_and_minutes() -> None:
    row: TimesheetsListRow = {
        "date": "2026-08-03",
        "user": {"id": 11, "external_id": "HR-1", "first_name": "Aisulu", "last_name": "Serik"},
        "planned": {"type": "work", "leave_type": None, "time_planned": 28800},  # type: ignore[typeddict-item]
        "actual": {"in": None, "out": None, "time_worked": 27000},  # type: ignore[typeddict-item]
        "variance": {
            "time_late": 180,
            "time_early_left": 0,
            "time_overworked": 0,
            "time_underworked": 1800,
        },
    }

    assert timesheet_export.line(row) == [
        "2026-08-03",
        "Serik Aisulu",
        "HR-1",
        "work",
        "8.00",
        "7.50",
        "3",
        "0",
        "0.00",
    ]


def test_a_day_nobody_was_scheduled_for_is_a_day_off() -> None:
    row: TimesheetsListRow = {
        "date": "2026-08-04",
        "user": {"id": 11, "external_id": "HR-1", "first_name": "Aisulu", "last_name": "Serik"},
        "planned": None,
    }

    written = timesheet_export.line(row)

    # The plan is what is absent, and the columns that describe one are left empty rather than nil.
    assert written[3] == "day off"
    assert written[4] == ""


def test_a_person_carries_only_what_the_file_says() -> None:
    row = {
        "external_id": "HR-1",
        "first_name": "Aisulu",
        "last_name": "",
        "email": "aisulu@example.com",
        "phone": "",
        "location_code": "WH-01",
    }

    written = roster_sync.person(row, {"WH-01": 100})

    # An empty column would otherwise blank a field somebody filled in the web application.
    assert written == {
        "external_id": "HR-1",
        "first_name": "Aisulu",
        "role": "employee",
        "location_id": 100,
        "email": "aisulu@example.com",
    }


def test_the_roster_is_written_a_hundred_at_a_time() -> None:
    person: UsersUpsertUser = {"first_name": "Aisulu", "role": "employee", "location_id": 1}
    batches = list(roster_sync.chunks([person] * 250))

    assert [len(batch) for batch in batches] == [100, 100, 50]
