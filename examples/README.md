# Examples

Two integrations of the shape most of them have: one writes a roster in, one reads a month out.
Both are single files, use the package as published, and need nothing beyond it.

```bash
pip install clockster
export CLOCKSTER_TOKEN=...   # Settings → API in the web application
```

## `roster_sync.py`

Sync employees from a CSV, and dismiss whoever is no longer in it.

```bash
python roster_sync.py people.csv
```

```csv
external_id,first_name,last_name,email,phone,location_code,location_title
HR-1,Aisulu,Serik,aisulu@example.com,+77010000001,WH-01,Warehouse
HR-2,Bolat,Nurlan,bolat@example.com,+77010000002,WH-01,Warehouse
```

What it shows: writing locations and reading their ids back out of the answer, `external_id` as the
key that makes a second run an update rather than a duplicate, batching at the hundred the endpoint
takes, and dismissing by difference — everybody active here who is not in the file.

Run it twice. The second run writes the same people and dismisses nobody, which is the property a
nightly sync needs.

## `timesheet_export.py`

Export a month of timesheets as CSV, a row per person per day.

```bash
python timesheet_export.py 2026-08 > august.csv
```

What it shows: paging with `paginate`, asking for the facts with `include`, and the two things that
catch people out — times are seconds, and a day nobody was scheduled for answers `planned: null`
rather than being left out.

## Writing your own

The methods are named after the operations, so the
[API documentation](https://api.clockster.com/openapi/v3.json) reads as the reference for both:
`GET /users` is `clockster.users.list(...)`, `POST /users/upsert` is `clockster.users.upsert(...)`.
Everything answers the parsed body and raises `ClocksterError` on a refusal.
