"""The operations of the Company API, as they are called.

Generated from openapi/company-v3.json — see scripts/generate.py. Every method answers the parsed
body of the response; a refusal is raised rather than returned, so there is no branch between the
call and the rows.
"""

from __future__ import annotations

from typing import IO, Any, Literal, cast

from .._transport import _AsyncNamespace, _AsyncTransport, _Namespace, _SyncTransport
from .models import *  # noqa: F403 - the answer types, by the names the document gives them

class PayrollPayslips(_Namespace):
    """`clockster.payroll.payslips`."""

    def list(self, *, per_page: int | None = None, cursor: str | None = None, users: list[int] | None = None, statuses: list[PayrollPayslipsStatus] | None = None, months: list[str] | None = None, updated_since: str | None = None) -> PayrollPayslipsListResponse:
        """List payslips

        Reading only. Nothing on this surface creates or changes a payslip.

        **Amounts carry their currency.** A payslip that carries none — one built from a salary
        filed before the field was required — answers the company's own currency rather than
        null, so you do not have to invent that fallback yourself.

        **The line items are here**: `additions`, `deductions` and `allowances`, each with its
        `title`, `value` and `pre_tax`, which is what decides whether an amount lands before tax
        is worked out.

        **`loan_repaid` is what was taken back against an advance.** An advance is not a
        deduction: it becomes a loan and is repaid on scheduled days, so it never appears in
        `deductions` and a caller subtracting the line items from the total will be out by
        exactly this amount. The figure folds together loan repayments and one-off loan
        adjustments, because that is how the calculation records them.

        **The parts do not add up to `take_home`, and are not meant to.** Taxes and the gross
        figure are not published here, so what you get is what was added, taken off and repaid —
        not a derivation of the total.

        **`updated_since` matters more here than anywhere**: a payslip is recalculated and moves
        from `draft` to `approved` to `paid`, so without it a caller re-reads every month
        forever. `months` is `YYYY-MM`, and takes a list, so a quarter is one request.
        """
        return cast(
            PayrollPayslipsListResponse,
            self._transport.request(
                "GET",
                "/company/v3/payroll/payslips",
                query={"per_page": per_page, "cursor": cursor, "users": users, "statuses": statuses, "months": months, "updated_since": updated_since},
            ),
        )


class PayrollSingleAdjustments(_Namespace):
    """`clockster.payroll.single_adjustments`."""

    def create(self, body: PayrollSingleAdjustmentsCreateBody, *, idempotency_key: str | None = None) -> PayrollSingleAdjustmentsCreateResponse:
        """Create single adjustments

        Up to 100 one-off amounts — a bonus, a service charge, a penalty — each for one person
        and one day. All or nothing: a `422` means none of the batch landed.

        **An adjustment is read when a payslip is calculated.** A `draft` payslip whose period
        holds `date` takes it in on its next calculation. An `approved` or `paid` one does not:
        it is recalculated only by hand in the web application, and nothing here tells you
        whether that happened. Check the payslip's status for the month before filing into it.

        **Send an `Idempotency-Key`.** An adjustment carries no key of yours, so a retry after a
        timeout files it a second time unless the header says it is the same attempt. The
        answer lists what was created, in the order sent.
        """
        return cast(
            PayrollSingleAdjustmentsCreateResponse,
            self._transport.request(
                "POST",
                "/company/v3/payroll/single-adjustments",
                json=body,
                idempotency_key=idempotency_key,
            ),
        )

    def delete(self, id: int) -> PayrollSingleAdjustmentsDeleteResponse:
        """Delete a single adjustment

        Deletes the adjustment. A payslip already calculated with it keeps the amount until it
        is calculated again — for an `approved` or `paid` one, only by hand in the web
        application.

        Another company's id is a `404`.
        """
        return cast(
            PayrollSingleAdjustmentsDeleteResponse,
            self._transport.request(
                "DELETE",
                f"/company/v3/payroll/single-adjustments/{id}",
            ),
        )

    def list(self, *, per_page: int | None = None, cursor: str | None = None, users: list[int] | None = None, types: list[PayrollSingleAdjustmentsType] | None = None, date_from: str | None = None, date_to: str | None = None) -> PayrollSingleAdjustmentsListResponse:
        """List single adjustments

        One-off additions and deductions, oldest first, with who they are for and the day they
        are dated.

        `amount` is never negative: `type` says whether it is added or taken off, and whether
        before or after tax. `date_from` and `date_to` bound the day, inclusive.

        Rows filed in the web application are listed too, and may carry `13th_pay`, which is
        computed there rather than filed here.
        """
        return cast(
            PayrollSingleAdjustmentsListResponse,
            self._transport.request(
                "GET",
                "/company/v3/payroll/single-adjustments",
                query={"per_page": per_page, "cursor": cursor, "users": users, "types": types, "date_from": date_from, "date_to": date_to},
            ),
        )


class WebhooksDeliveries(_Namespace):
    """`clockster.webhooks.deliveries`."""

    def get(self, id: int) -> WebhooksDeliveriesGetResponse:
        """Read one webhook delivery

        Answers with the payload, unlike the listing: one row is not a hundred employee records.
        """
        return cast(
            WebhooksDeliveriesGetResponse,
            self._transport.request(
                "GET",
                f"/company/v3/webhooks/deliveries/{id}",
            ),
        )

    def list(self, *, per_page: int | None = None, cursor: str | None = None, webhooks: list[int] | None = None, events: list[WebhooksEvent] | None = None, successful: bool | None = None, pending: bool | None = None, since: str | None = None, include: list[WebhooksDeliveriesInclude] | None = None) -> WebhooksDeliveriesListResponse:
        """List webhook deliveries

        What was sent, and what came of it. **Newest first**, unlike every other listing here: a
        delivery log is read to learn what just happened.

        `state` is the field to branch on. `delivered` and `failed` are final; `pending` is
        neither — the event is waiting out its backoff and will be tried again. Reading
        `is_successful: false` as failure is the mistake the two stored flags invite.

        `payload` is behind `include=payload` and off by default: a page of a hundred deliveries
        is a hundred employee records, and a caller watching its integration's health has no use
        for them. Reading one delivery answers with it either way.

        `webhook_id` is null where the endpoint has since been removed.
        """
        return cast(
            WebhooksDeliveriesListResponse,
            self._transport.request(
                "GET",
                "/company/v3/webhooks/deliveries",
                query={"per_page": per_page, "cursor": cursor, "webhooks": webhooks, "events": events, "successful": successful, "pending": pending, "since": since, "include": include},
            ),
        )

    def redeliver(self, id: int, *, idempotency_key: str | None = None) -> WebhooksDeliveriesRedeliverResponse:
        """Send a delivery again

        Queues the recorded event for another attempt, and answers once queued rather than once
        delivered.

        A repair tool, now that transient failures retry themselves: this is for the case where
        the receiver was fixed after we had already given up. What goes out is the event as it
        was recorded, so `occurred_at` may be long past — which is why the envelope states it.
        """
        return cast(
            WebhooksDeliveriesRedeliverResponse,
            self._transport.request(
                "POST",
                f"/company/v3/webhooks/deliveries/{id}/redeliver",
                idempotency_key=idempotency_key,
            ),
        )


class WebhooksEvents(_Namespace):
    """`clockster.webhooks.events`."""

    def list(self) -> WebhooksEventsListResponse:
        """List subscribable events

        Every event name an endpoint can subscribe to.

        Served as well as specified, so a caller can check at runtime that a name it stored is
        still one we send rather than discovering it on the next save.
        """
        return cast(
            WebhooksEventsListResponse,
            self._transport.request(
                "GET",
                "/company/v3/webhooks/events",
            ),
        )


class Attendance(_Namespace):
    """`clockster.attendance`."""

    def list(self, *, date_from: str | None = None, date_to: str | None = None, per_page: int | None = None, cursor: str | None = None, users: list[int] | None = None, locations: list[int] | None = None, statuses: list[AttendanceStatus] | None = None, sources: list[AttendanceSource] | None = None, include: list[AttendanceInclude] | None = None) -> AttendanceListResponse:
        """List clock-ins

        Marks inside a window of days, oldest first.

        **The window is required and capped at 90 days.** This is the largest table in the
        product; an unbounded read of it has no plan that finishes. `date_from` and `date_to`
        are plain dates matched against the clock the mark was stamped with, not against an
        instant — a day means the same thing here as it does to the person who worked it.

        **`datetime` is the moment as it was recorded**, offset included — the stored wall clock
        read in the stored zone, never shifted anywhere else. It is one field because it is one
        fact: the wall clock is the value without its offset, and the zone is the offset. On the
        rare row whose zone cannot be read it comes back with no offset at all, which is how you
        see that the zone was not known.

        `status` is `in`, `out` or `break`, not the integer the column keeps.

        Late arrivals are the one thing to plan for: a device that was offline uploads what it
        recorded earlier, so a mark can appear inside a window you have already read. Re-read
        the last few days with overlap rather than paging strictly forward and never looking
        back.
        """
        return cast(
            AttendanceListResponse,
            self._transport.request(
                "GET",
                "/company/v3/attendance",
                query={"date_from": date_from, "date_to": date_to, "per_page": per_page, "cursor": cursor, "users": users, "locations": locations, "statuses": statuses, "sources": sources, "include": include},
            ),
        )

    def record(self, body: AttendanceRecordBody) -> AttendanceRecordResponse:
        """Record attendance

        Marks recorded by something you run — a turnstile of your own, a kiosk, your app.

        **`datetime` carries its own offset and is the only place time is stated** — send
        `2026-08-10T09:03:00+05:00` and `09:03:00` goes on file with `+05:00` beside it. There
        is no separate timezone field, and the offset is not optional: the wall clock and the
        zone are read off that one value, so they cannot disagree. A mark may not be dated in the
        future, nor more than 24 hours back: older than that is history being rewritten, and
        lateness already computed against the day would move under it.

        `status` is `in`, `out` or `break`, and the answer echoes it back in those words, with
        the moment as the instant it was recorded at — the same shapes the listing answers with.

        **A mark already on file for the same person, moment and direction is not written
        again**, whether it repeats across two requests or inside one. There is no key you own
        on this resource, so no promise of idempotency is made in general — but a retried upload
        will not double somebody's day. The answer says `created` or `unchanged` per item, with
        the id either way.

        The shift a mark belongs to is worked out afterwards, so `shift_id` is yours to send
        only if you already know it.
        """
        return cast(
            AttendanceRecordResponse,
            self._transport.request(
                "POST",
                "/company/v3/attendance",
                json=body,
            ),
        )


class Departments(_Namespace):
    """`clockster.departments`."""

    def delete(self, id: int) -> DepartmentsDeleteResponse:
        """Delete a department

        **Refused while anybody is in it** — 409, `department_in_use`.

        Once it goes, so do its managers, and there is no way to reconstruct who was in it.

        Move the people first, then delete. Somebody dismissed does not count as being in it.
        """
        return cast(
            DepartmentsDeleteResponse,
            self._transport.request(
                "DELETE",
                f"/company/v3/departments/{id}",
            ),
        )

    def get(self, id: int, *, include: list[DepartmentsInclude] | None = None) -> DepartmentsGetResponse:
        """Read one department

        The same keys and the same `include` vocabulary as the listing — `include=managers` adds the managers. Somebody else's id is a `404`.
        """
        return cast(
            DepartmentsGetResponse,
            self._transport.request(
                "GET",
                f"/company/v3/departments/{id}",
                query={"include": include},
            ),
        )

    def list(self, *, per_page: int | None = None, cursor: str | None = None, search: str | None = None, updated_since: str | None = None, include: list[DepartmentsInclude] | None = None) -> DepartmentsListResponse:
        """List departments

        `include=managers` adds the managers. Without it the key is absent, never null standing in for "not asked for".
        """
        return cast(
            DepartmentsListResponse,
            self._transport.request(
                "GET",
                "/company/v3/departments",
                query={"per_page": per_page, "cursor": cursor, "search": search, "updated_since": updated_since, "include": include},
            ),
        )

    def upsert(self, body: DepartmentsUpsertBody) -> DepartmentsUpsertResponse:
        """Create or update departments

        Up to 100 entries in one call, matched on `external_id`.

        **Not matched on the name.** Renaming an entry on your side updates ours, where matching
        on `title` would have created a second and orphaned the first.
        """
        return cast(
            DepartmentsUpsertResponse,
            self._transport.request(
                "POST",
                "/company/v3/departments/upsert",
                json=body,
            ),
        )


class Documents(_Namespace):
    """`clockster.documents`."""

    def delete(self, id: int) -> DocumentsDeleteResponse:
        """Delete a document

        Deletes the document, its file records and the stored objects behind them.

        **A document everyone has signed cannot be deleted** — `409`, code `document_signed`.

        Another company's id is a `404`.
        """
        return cast(
            DocumentsDeleteResponse,
            self._transport.request(
                "DELETE",
                f"/company/v3/documents/{id}",
            ),
        )

    def get(self, id: int, *, include: list[DocumentsInclude] | None = None) -> DocumentsGetResponse:
        """Read one document

        The same keys the listing answers with, and the same `include` vocabulary. Another company's id is a `404`.
        """
        return cast(
            DocumentsGetResponse,
            self._transport.request(
                "GET",
                f"/company/v3/documents/{id}",
                query={"include": include},
            ),
        )

    def list(self, *, per_page: int | None = None, cursor: str | None = None, party: DocumentsParty | None = None, external_ids: list[str] | None = None, users: list[int] | None = None, locations: list[int] | None = None, departments: list[int] | None = None, positions: list[int] | None = None, user_filters: list[int] | None = None, types: list[DocumentsType] | None = None, employment_types: list[DocumentsEmploymentType] | None = None, search: str | None = None, updated_since: str | None = None, expires_after: str | None = None, expires_before: str | None = None, effective_from: str | None = None, effective_to: str | None = None, include: list[DocumentsInclude] | None = None) -> DocumentsListResponse:
        """List documents

        The company's paperwork, oldest first, paged on a cursor.

        **Both kinds of document.** `party` is `employee` for a document about one of your
        people and `counterparty` for one a counterparty signs. Filter with `party=employee` or
        `party=counterparty`; leave it out for both.

        **`signature.state` is derived, because there is no column for it.** `none` when nobody
        has to sign, then `rejected`, `revoked`, `pending` in that order of precedence, and
        `signed` only when every signer has. Refusal outranks an outstanding signature, so a
        document one person refused reads `rejected` even while others are still pending.
        `completed_at` is set only for `signed`, and is when the last signer signed.

        **Dates are three shapes in one payload.** `start_date`, `end_date` and
        `expiration_date` are plain `YYYY-MM-DD` — they are date columns and carry no time or
        zone. `created_at` is an instant with an offset.

        `expires_after` and `expires_before` are a plain range of dates.

        `effective_from` and `effective_to` select documents valid during a window: a document
        starts on or before your `effective_to` and either has no end date or ends on or after
        your `effective_from`. Both are required together. **A document with no `start_date`
        never matches** — a row with no interval cannot overlap one.

        `locations`, `departments`, `positions` and `user_filters` all reach the document
        through the person it is about, so **a document with no `user_id` matches none of
        them**. The web app files company-level documents that way.

        **`updated_since` reads only what changed**, as an instant rather than a date so a
        caller polling every few minutes can say which minute. Two things it will not show you,
        and both are ours rather than yours: a document changed by a path inside the product
        that writes the row directly keeps its old timestamp, and so does one the back office
        modifies. Signature progress is the common case of the second — a signature completed
        through the web app does not move `updated_at`. Re-read with overlap if you depend on
        catching those.

        Documents the product files for its own machinery are never listed.
        """
        return cast(
            DocumentsListResponse,
            self._transport.request(
                "GET",
                "/company/v3/documents",
                query={"per_page": per_page, "cursor": cursor, "party": party, "external_ids": external_ids, "users": users, "locations": locations, "departments": departments, "positions": positions, "user_filters": user_filters, "types": types, "employment_types": employment_types, "search": search, "updated_since": updated_since, "expires_after": expires_after, "expires_before": expires_before, "effective_from": effective_from, "effective_to": effective_to, "include": include},
            ),
        )

    def upsert(self, body: DocumentsUpsertBody) -> DocumentsUpsertResponse:
        """File documents

        Up to 100 documents in one call, matched on `external_id`, which is required here.

        **The bytes go up separately.** `POST /company/v3/files` takes one file and answers an
        id; send that as `file_id`. A file may be claimed once: one already hanging off a
        document is refused rather than moved.

        **An uploaded file waits to be claimed and is not cleaned up.** A batch refused at the
        hundredth document leaves all hundred files staged and still valid, so a retry should
        send the same `file_id`s rather than uploading them again.

        `parent_external_id` links a supplementary agreement to what it amends, by your key
        rather than ours. It resolves against documents already filed — not against another item
        of the same batch — and a key matching nothing clears the link rather than failing.

        `user_id` is required and may name somebody who has left: termination paperwork is filed
        after a dismissal, which is exactly when it is needed.

        **No signers.** Signing runs conversions and outbound calls that do not belong under a
        versioned contract, so documents filed here are always `party: employee`. Signature
        state is readable; creating a signing request is not offered yet.

        `author_id` is set to the subject: this token authenticates a company, not a person.
        """
        return cast(
            DocumentsUpsertResponse,
            self._transport.request(
                "POST",
                "/company/v3/documents/upsert",
                json=body,
            ),
        )


class Files(_Namespace):
    """`clockster.files`."""

    def upload(self, file: bytes | IO[bytes], *, filename: str = "upload", name: str | None = None) -> FilesUploadResponse:
        """Upload a file

        One file, `multipart/form-data`, field name `file`. The only route on this surface that
        is not JSON.

        It answers an `id`. That id is what `POST /company/v3/documents/upsert` takes as
        `file_id`; until a document claims it the file belongs to nothing.

        Up to 10 MB. `pdf`, `doc`, `docx`, `xls`, `xlsx`, `jpg`, `jpeg`, `png` — the content is
        checked, not just the extension. `name` is optional and defaults to the uploaded
        filename without its extension.

        `url` is signed and short-lived: read it, do not store it. Read the document again to
        get a fresh one.
        """
        return cast(
            FilesUploadResponse,
            self._transport.request(
                "POST",
                "/company/v3/files",
                files={"file": (filename, file)},
                data={"name": name},
            ),
        )


class Locations(_Namespace):
    """`clockster.locations`."""

    def delete(self, id: int) -> LocationsDeleteResponse:
        """Delete a location

        **Refused while anybody works there** — 409, `location_in_use` — counting both the
        location on a person's record and the several they may also be assigned to.

        **Refused while anything sits beneath it** — 409, `location_has_children`. Deleting a
        parent detaches its whole subtree and destroys the rows describing the ancestry, and
        this API cannot express a hierarchy at all, so you would not be able to see what you
        had taken apart.

        Once it goes, so do its managers, its device assignments and any auto-scheduler
        configured for it; devices, schedules, tasks and approval routes keep working with the
        location set to null. None of that is recoverable and none of it is logged.

        Move the people first, then delete.
        """
        return cast(
            LocationsDeleteResponse,
            self._transport.request(
                "DELETE",
                f"/company/v3/locations/{id}",
            ),
        )

    def get(self, id: int, *, include: list[LocationsInclude] | None = None) -> LocationsGetResponse:
        """Read one location

        The same keys the listing answers with. Somebody else's id is a `404`, where asking the listing for it answers `200` with an empty array and leaves you counting.
        """
        return cast(
            LocationsGetResponse,
            self._transport.request(
                "GET",
                f"/company/v3/locations/{id}",
                query={"include": include},
            ),
        )

    def list(self, *, per_page: int | None = None, cursor: str | None = None, search: str | None = None, include: list[LocationsInclude] | None = None, codes: list[str] | None = None, updated_since: str | None = None) -> LocationsListResponse:
        """List locations

        Ordered by `id` and paged on a cursor: no page number, no total, and nothing repeated
        or skipped while the list is written to. A cursor issued for another ordering is
        refused rather than silently restarting the list.

        Coordinates are numbers, and a latitude of exactly 0 is a coordinate rather than a
        missing one.

        `include=managers` adds the employees who manage the location, as on departments and
        user filters.
        """
        return cast(
            LocationsListResponse,
            self._transport.request(
                "GET",
                "/company/v3/locations",
                query={"per_page": per_page, "cursor": cursor, "search": search, "include": include, "codes": codes, "updated_since": updated_since},
            ),
        )

    def upsert(self, body: LocationsUpsertBody) -> LocationsUpsertResponse:
        """Create or update locations

        Up to 100 entries in one call, matched on `external_id`.

        **Not matched on the name.** Renaming an entry on your side updates ours, where matching
        on `title` would have created a second and orphaned the first.

        `code` and `external_id` are different things and both are kept: `code` is a label you
        fill in and we never validate, `external_id` is what the match runs on. Coordinates and
        radius are set here too.
        """
        return cast(
            LocationsUpsertResponse,
            self._transport.request(
                "POST",
                "/company/v3/locations/upsert",
                json=body,
            ),
        )


class Payroll(_Namespace):
    """`clockster.payroll`."""

    def __init__(self, transport: _SyncTransport) -> None:
        super().__init__(transport)
        self.payslips = PayrollPayslips(transport)
        self.single_adjustments = PayrollSingleAdjustments(transport)


class Positions(_Namespace):
    """`clockster.positions`."""

    def delete(self, id: int) -> PositionsDeleteResponse:
        """Delete a position

        **Refused while anybody holds it** — 409, `position_in_use`.

        Beyond the people: deleting a position destroys its auto-scheduler staffing
        configuration outright, so a rota that says "two bakers on nights" stops saying it.

        Move the people first, then delete.
        """
        return cast(
            PositionsDeleteResponse,
            self._transport.request(
                "DELETE",
                f"/company/v3/positions/{id}",
            ),
        )

    def get(self, id: int, *, include: list[str] | None = None) -> PositionsGetResponse:
        """Read one position

        The same keys the listing answers with. A position carries no managers, so asking to include them is refused rather than answered with an empty list.
        """
        return cast(
            PositionsGetResponse,
            self._transport.request(
                "GET",
                f"/company/v3/positions/{id}",
                query={"include": include},
            ),
        )

    def list(self, *, per_page: int | None = None, cursor: str | None = None, search: str | None = None, updated_since: str | None = None, include: list[str] | None = None) -> PositionsListResponse:
        """List positions

        A position carries no managers, so asking to include them is refused rather than answered with an empty list.
        """
        return cast(
            PositionsListResponse,
            self._transport.request(
                "GET",
                "/company/v3/positions",
                query={"per_page": per_page, "cursor": cursor, "search": search, "updated_since": updated_since, "include": include},
            ),
        )

    def upsert(self, body: PositionsUpsertBody) -> PositionsUpsertResponse:
        """Create or update positions

        Up to 100 entries in one call, matched on `external_id`.

        **Not matched on the name.** Renaming an entry on your side updates ours, where matching
        on `title` would have created a second and orphaned the first.
        """
        return cast(
            PositionsUpsertResponse,
            self._transport.request(
                "POST",
                "/company/v3/positions/upsert",
                json=body,
            ),
        )


class Schedules(_Namespace):
    """`clockster.schedules`."""

    def create(self, body: SchedulesCreateBody, *, idempotency_key: str | None = None) -> SchedulesCreateResponse:
        """Create schedules

        Up to 25 schedules in one call, each a kind of day, the days it falls on, and the people
        it is for. `type` is per item, so a rota and the absences inside it go together.

        There are no repeat patterns: send the dates. If you want every Monday, say which
        Mondays.

        **Send the rota as one call, not as twenty.** Everyone named is notified, once per call —
        so the same twenty schedules sent one at a time buzz in somebody's pocket twenty times.

        **This is the write to send an `Idempotency-Key` with.** A schedule carries no key of
        yours, so a retry after a timeout files the rota a second time unless the header tells us
        it is the same attempt.

        **Schedules carry no key you own**, so a resend duplicates rather than converges. A
        `422` means none of the batch landed and is safe to fix and send again; a timeout is
        not — read back before retrying. The answer lists what was created, in the order sent.

        **`type` decides what else is required.** `work` needs `timezone` and either
        `start`/`end` or `shifts`. `free` — a day with hours to make up rather than hours to
        keep — needs `timezone`, `start`, `end`, and takes `time_planned`. `leave` needs only
        `leave_type`.

        `start` and `end` are clock times, `HH:MM:SS`, read in `timezone` — not instants, whatever
        a generated client calls the field. `timezone` is a fixed offset, `+05:00` or `Z`.

        **The answer is not an echo of the request, so read it.** A day with two or more `shifts`
        takes its `start`, `end` and `time_planned` from them and comes back with `is_split`
        true. A day with exactly one shift is not a split day: the hours move onto the day itself
        and `shifts` comes back empty. `time_planned` for a worked day is always computed —
        the hours less the break — never taken from what you sent.

        **Every span is seconds**, `break_time` and `grace_start`/`grace_end` included. Grace is
        stored to the minute, so send a multiple of 60; the maximum is 3600.

        **Grace is not the same as a boundary.** It is how far past the start a person may arrive
        and still be credited from the shift boundary. How far outside the shift a punch is
        collected at all is a company setting and is not on this endpoint.

        There is no `title` — one is generated and it means nothing to you. One schedule takes up
        to 366 dates, 200 people and 8 shifts.
        """
        return cast(
            SchedulesCreateResponse,
            self._transport.request(
                "POST",
                "/company/v3/schedules",
                json=body,
                idempotency_key=idempotency_key,
            ),
        )

    def delete(self, id: int) -> SchedulesDeleteResponse:
        """Delete a schedule

        Everyone who was on it is notified, the same way a change to it would notify them.

        **A default schedule is refused** — 409, `schedule_is_default`. It is what the company
        falls back to.

        **An open shift is refused** — 409, `schedule_is_open`. Deleting one also removes its
        siblings and recomputes their days, which this API can neither create nor show you. Use
        the web application.
        """
        return cast(
            SchedulesDeleteResponse,
            self._transport.request(
                "DELETE",
                f"/company/v3/schedules/{id}",
            ),
        )

    def get(self, id: int) -> SchedulesGetResponse:
        """Read one schedule

        Exactly what creating it answered with — the same keys, the shifts and the people
        included, since those are the schedule rather than an optional extra.

        Worth reading back after a create: a day with two or more shifts takes its `start`,
        `end` and `time_planned` from them, and a day with exactly one has the shift folded into
        it and comes back with `shifts` empty.

        There is no listing of schedules. `GET /company/v3/timesheets` answers what a person is
        scheduled for on a day, which is the question a rota is usually asked.
        """
        return cast(
            SchedulesGetResponse,
            self._transport.request(
                "GET",
                f"/company/v3/schedules/{id}",
            ),
        )


class Tasks(_Namespace):
    """`clockster.tasks`."""

    def get(self, id: int, *, include: list[TasksInclude] | None = None) -> TasksGetResponse:
        """Read one task

        The same keys the listing answers with, and the same `include` vocabulary. Another company's id is a `404`.
        """
        return cast(
            TasksGetResponse,
            self._transport.request(
                "GET",
                f"/company/v3/tasks/{id}",
                query={"include": include},
            ),
        )

    def list(self, *, per_page: int | None = None, cursor: str | None = None, external_ids: list[str] | None = None, users: list[int] | None = None, categories: list[int] | None = None, statuses: list[TasksStatus] | None = None, active: bool | None = None, search: str | None = None, due_from: str | None = None, due_to: str | None = None, updated_since: str | None = None, include: list[TasksInclude] | None = None) -> TasksListResponse:
        """List tasks

        Work as we hold it: what was issued, what became of it, and how it measured up.

        `kpi_fact` against `kpi_plan`, plus `time_worked`, are the point of reading a task back
        — what was asked for, what was achieved, how long it took. `status` says where it got
        to.

        **Twenty-four fields, not the forty the table has.** Eight of the rest configure how the
        mobile application behaves while the job is done — whether it demands a photo, records a
        location, keeps the steps in order. That is a task template's business, and neither
        useful nor settable here.

        `include=items` adds the steps, `include=managers` the people who approve or are
        notified. Without them the keys are absent, never null standing in for "not asked for".

        **`updated_since` is what an export should page on**, as an instant: a task moves
        through its statuses inside a working day, so a caller polling for completions needs to
        say which minute.

        `statuses` takes `created`, `started`, `paused`, `completed`, `incompleted` and
        `pastdue`. Three more exist in the database and none is offered: `finished` and
        `unfinished` are deprecated spellings, and `pending` is reached only through approval.
        A value that cannot be explained is worse than one that is absent.

        **Oldest first.** A first call lands on the earliest task this company ever issued,
        which for a long-standing one is years back. That order is what lets a full export
        finish in one walk, and it is not what you want for "what happened lately": ask with
        `updated_since`, or narrow with `due_from` and `due_to`.
        """
        return cast(
            TasksListResponse,
            self._transport.request(
                "GET",
                "/company/v3/tasks",
                query={"per_page": per_page, "cursor": cursor, "external_ids": external_ids, "users": users, "categories": categories, "statuses": statuses, "active": active, "search": search, "due_from": due_from, "due_to": due_to, "updated_since": updated_since, "include": include},
            ),
        )

    def upsert(self, body: TasksUpsertBody) -> TasksUpsertResponse:
        """Issue tasks

        Up to 100 pieces of work in one call, matched on `external_id`, which is required here
        — a task has no natural key of its own, since the same round is issued every week under
        the same title.

        **`status` is not accepted, and neither are the timestamps around it.** The product
        moves a task through its lifecycle with events — completing notifies, approval routes,
        reopening makes it pastdue again — and a status written straight onto the row fires none
        of that. Issue the work here; read where it got to with `GET /company/v3/tasks`.

        **Eight fields are not accepted either** — `req_photo`, `req_sequence`, `gallery`,
        `get_location`, `get_timing`, `is_keep_status`, `req_approve`, `req_notify`. They
        configure the mobile application, not the job.

        **Where the work sits is taken from whoever it is for.** Omit `location_id`,
        `department_id` and `position_id` and they come from the assignee — your system knows
        the person, not our org chart. Send them to override.

        **`items` is an exception to the omitted-field rule**: sending it replaces the steps outright, because a step carries no key
        to match an incoming one against — and replacing them discards the completion the person
        doing the work recorded. Omit the key to leave them alone. `managers` likewise states
        who approves now rather than adding to them.

        `kpi_plan` has no "unset" — the column is NOT NULL with a default of 0, so an omitted
        plan is a plan of zero.
        """
        return cast(
            TasksUpsertResponse,
            self._transport.request(
                "POST",
                "/company/v3/tasks/upsert",
                json=body,
            ),
        )


class Timesheets(_Namespace):
    """`clockster.timesheets`."""

    def list(self, *, date_from: str | None = None, date_to: str | None = None, cursor: str | None = None, users: list[int] | None = None, locations: list[int] | None = None, departments: list[int] | None = None, positions: list[int] | None = None, employment: str | None = None, include: list[TimesheetsInclude] | None = None) -> TimesheetsListResponse:
        """Timesheets

        One row per person per calendar day of the window: what was planned, and — when asked
        for — what happened and how the two differ.

        **`planned` alone is the timesheet grid** — who was meant to work, when, and what kind
        of day it was. `include=actual` adds what was recorded, `include=variance` adds the
        difference. Either one is what makes the request expensive, because both require
        matching the clock-ins.

        **The four variance numbers are not additive.** Arriving three minutes late produces
        `time_late` 180 and `time_underworked` 180 — the same minutes, counted once as lateness
        and once as unfilled plan. Summing them double-counts.

        **`planned: null` means no schedule at all for that day.** It is rarer than it sounds: a
        company created with default settings carries a work and a leave schedule covering four
        years, so ordinary days off arrive as `type: leave` rather than as an absent plan. A day
        that was scheduled and not worked is the other case — a plan, an empty `actual`, and
        `time_underworked` equal to the whole planned time.

        **There is no `per_page`.** How many rows fifty people produce depends on the window and
        on who is scheduled, which the caller cannot predict and we can: the page is sized to a
        row budget instead, and `meta.users_per_page` reports what that came to. Paging walks
        people, so one person's whole period always arrives on a single page and a monthly total
        never has to be assembled across two.

        Holidays are not marked: take them from your own calendar. Drafts are never returned.
        """
        return cast(
            TimesheetsListResponse,
            self._transport.request(
                "GET",
                "/company/v3/timesheets",
                query={"date_from": date_from, "date_to": date_to, "cursor": cursor, "users": users, "locations": locations, "departments": departments, "positions": positions, "employment": employment, "include": include},
            ),
        )


class UserFilters(_Namespace):
    """`clockster.user_filters`."""

    def delete(self, id: int) -> UserFiltersDeleteResponse:
        """Delete a user filter

        Members do not block it — a filter is a label, and a caller who keeps their filters in
        step re-creates it on the next sync.

        **Refused while an approval route points at it** — 409, `user_filter_in_use`. The route
        would survive with nobody to approve through it and quietly stop routing. Change the
        route first.
        """
        return cast(
            UserFiltersDeleteResponse,
            self._transport.request(
                "DELETE",
                f"/company/v3/user-filters/{id}",
            ),
        )

    def get(self, id: int, *, include: list[UserFiltersInclude] | None = None) -> UserFiltersGetResponse:
        """Read one user filter

        The same keys and the same `include` vocabulary as the listing. Somebody else's id is a `404`.
        """
        return cast(
            UserFiltersGetResponse,
            self._transport.request(
                "GET",
                f"/company/v3/user-filters/{id}",
                query={"include": include},
            ),
        )

    def list(self, *, per_page: int | None = None, cursor: str | None = None, search: str | None = None, updated_since: str | None = None, include: list[UserFiltersInclude] | None = None) -> UserFiltersListResponse:
        """List user filters

        `include=managers` adds the managers, as on departments.
        """
        return cast(
            UserFiltersListResponse,
            self._transport.request(
                "GET",
                "/company/v3/user-filters",
                query={"per_page": per_page, "cursor": cursor, "search": search, "updated_since": updated_since, "include": include},
            ),
        )

    def upsert(self, body: UserFiltersUpsertBody) -> UserFiltersUpsertResponse:
        """Create or update user filters

        Up to 100 entries in one call, matched on `external_id`.

        **Not matched on the name.** Renaming an entry on your side updates ours, where matching
        on `title` would have created a second and orphaned the first.
        """
        return cast(
            UserFiltersUpsertResponse,
            self._transport.request(
                "POST",
                "/company/v3/user-filters/upsert",
                json=body,
            ),
        )


class UserRequests(_Namespace):
    """`clockster.user_requests`."""

    def get(self, id: int) -> UserRequestsGetResponse:
        """Read one request

        Answers with `content`, unlike the listing: one row is one shape to make sense of, not a hundred.
        """
        return cast(
            UserRequestsGetResponse,
            self._transport.request(
                "GET",
                f"/company/v3/user-requests/{id}",
            ),
        )

    def list(self, *, per_page: int | None = None, cursor: str | None = None, types: list[UserRequestsType] | None = None, statuses: list[UserRequestsStatus] | None = None, subtypes: list[str] | None = None, users: list[int] | None = None, updated_since: str | None = None, include: list[UserRequestsInclude] | None = None) -> UserRequestsListResponse:
        """List requests

        What people asked for, and what became of it — leave, schedule changes, corrections and
        money.

        **Read this to learn that a timesheet moved.** Half of everything here is a batch
        clock-in correction: somebody forgot to punch, a manager approved the fix, and the
        attendance for those days changed after the fact. Only 48 per cent of those are approved
        within three days of the day they correct, and a third reach back more than a week — so
        a caller that pulled a timesheet last week cannot assume it still holds. Attendance
        carries no timestamps of its own, which makes this listing paged on `updated_since` the
        only signal that anything has moved.

        `period` is the field that makes that usable: the span of days a request concerns,
        wherever its kind happens to keep them. A clock-in correction keeps them inside the
        punches, a leave request as a period or a list, a request for a certificate not at all —
        both ends are null there rather than invented.

        `subtype` is the second half of `type`, and the product keeps it in two different places
        — `content.type` for most kinds, `content.leave_type` for leave. It is answered as one
        field, and `subtypes` filters on both.

        `comment` is what the author wrote when filing it, ordinarily the reason. Comments the
        workflow writes itself — on acknowledgement, or when a spawned task closes — are not
        answered here.

        **Oldest first.** A first call lands on the earliest request this company ever filed,
        which for a long-standing one is years back. That order is what lets a full export
        finish in one walk, and it is not what you want for "what changed lately": ask with
        `updated_since`.

        `content` is behind `include=content`: its shape depends on the kind, and one schema
        describes one shape everywhere else on this surface.

        **Reading only.** Creating a request enters a workflow — approval routes resolve,
        approvers are notified, tasks are spawned — and approving one is a person's decision that
        a dismissal application or a sick note gives weight to.
        """
        return cast(
            UserRequestsListResponse,
            self._transport.request(
                "GET",
                "/company/v3/user-requests",
                query={"per_page": per_page, "cursor": cursor, "types": types, "statuses": statuses, "subtypes": subtypes, "users": users, "updated_since": updated_since, "include": include},
            ),
        )


class Users(_Namespace):
    """`clockster.users`."""

    def dismiss(self, body: UsersDismissBody) -> UsersDismissResponse:
        """Dismiss employees

        Up to 100 people in one call, each named by `external_id` or by `id`, exactly one per
        item.

        **This is dismissal, not erasure.** The record stays and stays readable: the person
        appears under `status=dismissed` with `dismissed_at` set, and the seat is freed for
        somebody else. It is the shape leaving actually has — a nightly sync noticing that
        twelve people are no longer on the roster.

        **There is no hard delete on this API.** Erasing a person takes their attendance,
        payroll, documents and bank details with them, with no way to undo it, and one ability
        grants this whole API — an integrator that syncs your roster cannot be given that
        without also being given erasure. If a retention obligation needs it, ask us.

        **Somebody already gone answers `already_dismissed`** rather than failing, which matters
        here because dismissing frees the key for a new hire.

        **If a key is held by two people** — one who left and one hired since — the living one
        is the one dismissed.

        What happens that you cannot see, and cannot undo:

        - Their sessions end immediately and their phone is unpaired.
        - Every terminal at their locations is told to forget their face. That is sent once and
          not retried, so a terminal that is offline at the time keeps admitting them.
        - **Requests still waiting on them to approve are cancelled**, not just their own. Dismiss
          a manager and their team's pending vacation requests are cancelled with them.
        - An offboarding process starts, if the company has one configured.
        - `date_leave` is filled in with today's date if it was empty.
        """
        return cast(
            UsersDismissResponse,
            self._transport.request(
                "POST",
                "/company/v3/users/dismiss",
                json=body,
            ),
        )

    def get(self, id: int, *, include: list[UsersInclude] | None = None) -> UsersGetResponse:
        """Read one employee

        One employee by our id. Prefer it over `?ids=` when you expect exactly one: someone who
        is not yours answers `404`, where the listing answers `200` with an empty array, so a
        status can be branched on without counting.

        Reachable for a dismissed person too.
        """
        return cast(
            UsersGetResponse,
            self._transport.request(
                "GET",
                f"/company/v3/users/{id}",
                query={"include": include},
            ),
        )

    def list(self, *, per_page: int | None = None, cursor: str | None = None, search: str | None = None, updated_since: str | None = None, status: UsersStatus | None = None, ids: list[int] | None = None, codes: list[str] | None = None, external_ids: list[str] | None = None, locations: list[int] | None = None, departments: list[int] | None = None, positions: list[int] | None = None, user_filters: list[int] | None = None, employment: list[UsersEmployment] | None = None, include: list[UsersInclude] | None = None) -> UsersListResponse:
        """List employees

        The roster as we hold it. Every scalar is always present; a relation appears only when
        `include` names it.

        **`status` decides whether the people who left are in the answer** — `active` by
        default, `dismissed` for only them, `all` for both. A dismissed employee keeps their
        record: `date_leave` says when they were let go and `dismissed_at` when the record was
        closed. A sync that never asks for them cannot learn that anyone left, so ask
        periodically even if your day-to-day reads are `active`.

        **`external_ids` is the other half of the roster write.** Ask with the same keys you
        sent to `/users/upsert` and reconcile without keeping a map of our ids.

        `updated_since` reads only what changed, against the `updated_at` every row carries.
        """
        return cast(
            UsersListResponse,
            self._transport.request(
                "GET",
                "/company/v3/users",
                query={"per_page": per_page, "cursor": cursor, "search": search, "updated_since": updated_since, "status": status, "ids": ids, "codes": codes, "external_ids": external_ids, "locations": locations, "departments": departments, "positions": positions, "user_filters": user_filters, "employment": employment, "include": include},
            ),
        )

    def upsert(self, body: UsersUpsertBody) -> UsersUpsertResponse:
        """Create or update employees

        The roster, written in batches of up to 100. `external_id` is optional here and behaves
        as it does everywhere: an item carrying one updates the person it names, an item without
        one always creates. `first_name`, `role` and `location_id` are the minimum.

        The field set is what an HR system holds about an employee.

        A person created here reaches the turnstiles of their location, and every location's
        devices are told once for the whole batch rather than once per person.
        """
        return cast(
            UsersUpsertResponse,
            self._transport.request(
                "POST",
                "/company/v3/users/upsert",
                json=body,
            ),
        )


class Webhooks(_Namespace):
    """`clockster.webhooks`."""

    def __init__(self, transport: _SyncTransport) -> None:
        super().__init__(transport)
        self.deliveries = WebhooksDeliveries(transport)
        self.events = WebhooksEvents(transport)

    def create(self, body: WebhooksCreateBody, *, idempotency_key: str | None = None) -> WebhooksCreateResponse:
        """Create a webhook endpoint

        Connect an endpoint. Answers 201 with the signing secret it will use.

        **No `external_id`, and no upsert**, unlike every other write on this surface. Those
        mirror something your system already holds and must match on its own key; an endpoint is
        created here and its identity is ours, so there is nothing to match against.

        The secret is generated, never accepted: a caller-chosen signing key is a caller-chosen
        weakness. Replace it with `POST /company/v3/webhooks/{id}/secret`.

        Deliveries carry `X-Clockster-Event`, `X-Clockster-Delivery` (constant across retries,
        so a repeat can be recognised), `X-Clockster-Timestamp` and `X-Clockster-Signature` —
        `sha256=` HMAC-SHA256 of `timestamp + "." + rawBody` under the secret. The body is
        `{"id", "event", "occurred_at", "data"}`.
        """
        return cast(
            WebhooksCreateResponse,
            self._transport.request(
                "POST",
                "/company/v3/webhooks",
                json=body,
                idempotency_key=idempotency_key,
            ),
        )

    def delete(self, id: int) -> WebhooksDeleteResponse:
        """Delete a webhook endpoint

        Removes the endpoint. What was delivered to it stays readable: the delivery's link is
        nulled rather than cascaded, because the record of what was sent is the company's.
        """
        return cast(
            WebhooksDeleteResponse,
            self._transport.request(
                "DELETE",
                f"/company/v3/webhooks/{id}",
            ),
        )

    def get(self, id: int) -> WebhooksGetResponse:
        """Read one webhook endpoint
        """
        return cast(
            WebhooksGetResponse,
            self._transport.request(
                "GET",
                f"/company/v3/webhooks/{id}",
            ),
        )

    def list(self, *, per_page: int | None = None, cursor: str | None = None, active: bool | None = None) -> WebhooksListResponse:
        """List webhook endpoints

        The endpoints this company has connected, and the health of each.

        `health` answers what `active` cannot: whether a person switched an endpoint off or a
        run of failures did. Five consecutive permanent failures — a wrong address, refused
        credentials — switch it off, as do twenty transient ones. `disabled_reason` says which.

        `secret` is answered in full because verifying a signature is impossible without it.
        The credential we authenticate to the receiver *with* is not: `auth` names the scheme
        and, for basic, the username, and never the password or bearer token.
        """
        return cast(
            WebhooksListResponse,
            self._transport.request(
                "GET",
                "/company/v3/webhooks",
                query={"per_page": per_page, "cursor": cursor, "active": active},
            ),
        )

    def rotate_secret(self, id: int, *, idempotency_key: str | None = None) -> WebhooksRotateSecretResponse:
        """Replace the signing secret

        Answers the endpoint with a new secret.

        **Send an `Idempotency-Key`.** The secret is shown once, so a retry after a lost
        response would rotate a second time and leave you holding one that signs nothing — with
        the header, the retry is answered with the secret the first call minted.

        Deliveries already queued are signed with whichever secret is current when they are
        actually sent, so accept both for as long as your backlog can be deep — up to about a
        day where transient failures are being retried.
        """
        return cast(
            WebhooksRotateSecretResponse,
            self._transport.request(
                "POST",
                f"/company/v3/webhooks/{id}/secret",
                idempotency_key=idempotency_key,
            ),
        )

    def update(self, id: int, body: WebhooksUpdateBody) -> WebhooksUpdateResponse:
        """Replace a webhook endpoint

        Replaces rather than patches: half a subscription is not a state worth reaching by
        accident.

        Saving clears the failure tally and any automatic switch-off — you are saying something
        changed, so what the history counted no longer describes what is there. This is how an
        endpoint switched off by repeated failures is put back into service.
        """
        return cast(
            WebhooksUpdateResponse,
            self._transport.request(
                "PUT",
                f"/company/v3/webhooks/{id}",
                json=body,
            ),
        )


class _ClocksterApi(_Namespace):
    def __init__(self, transport: _SyncTransport) -> None:
        super().__init__(transport)
        self.attendance = Attendance(transport)
        self.departments = Departments(transport)
        self.documents = Documents(transport)
        self.files = Files(transport)
        self.locations = Locations(transport)
        self.payroll = Payroll(transport)
        self.positions = Positions(transport)
        self.schedules = Schedules(transport)
        self.tasks = Tasks(transport)
        self.timesheets = Timesheets(transport)
        self.user_filters = UserFilters(transport)
        self.user_requests = UserRequests(transport)
        self.users = Users(transport)
        self.webhooks = Webhooks(transport)

    def me(self) -> MeResponse:
        """Whose token this is

        Confirms which company a key belongs to.

        Answers the id and the name, and nothing else: everything a key opens is reachable from
        the endpoints themselves, and a company attribute this surface does not act on would
        only read as one it does.
        """
        return cast(
            MeResponse,
            self._transport.request(
                "GET",
                "/company/v3/me",
            ),
        )


class AsyncPayrollPayslips(_AsyncNamespace):
    """`clockster.payroll.payslips`."""

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, users: list[int] | None = None, statuses: list[PayrollPayslipsStatus] | None = None, months: list[str] | None = None, updated_since: str | None = None) -> PayrollPayslipsListResponse:
        """List payslips

        Reading only. Nothing on this surface creates or changes a payslip.

        **Amounts carry their currency.** A payslip that carries none — one built from a salary
        filed before the field was required — answers the company's own currency rather than
        null, so you do not have to invent that fallback yourself.

        **The line items are here**: `additions`, `deductions` and `allowances`, each with its
        `title`, `value` and `pre_tax`, which is what decides whether an amount lands before tax
        is worked out.

        **`loan_repaid` is what was taken back against an advance.** An advance is not a
        deduction: it becomes a loan and is repaid on scheduled days, so it never appears in
        `deductions` and a caller subtracting the line items from the total will be out by
        exactly this amount. The figure folds together loan repayments and one-off loan
        adjustments, because that is how the calculation records them.

        **The parts do not add up to `take_home`, and are not meant to.** Taxes and the gross
        figure are not published here, so what you get is what was added, taken off and repaid —
        not a derivation of the total.

        **`updated_since` matters more here than anywhere**: a payslip is recalculated and moves
        from `draft` to `approved` to `paid`, so without it a caller re-reads every month
        forever. `months` is `YYYY-MM`, and takes a list, so a quarter is one request.
        """
        return cast(
            PayrollPayslipsListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/payroll/payslips",
                query={"per_page": per_page, "cursor": cursor, "users": users, "statuses": statuses, "months": months, "updated_since": updated_since},
            ),
        )


class AsyncPayrollSingleAdjustments(_AsyncNamespace):
    """`clockster.payroll.single_adjustments`."""

    async def create(self, body: PayrollSingleAdjustmentsCreateBody, *, idempotency_key: str | None = None) -> PayrollSingleAdjustmentsCreateResponse:
        """Create single adjustments

        Up to 100 one-off amounts — a bonus, a service charge, a penalty — each for one person
        and one day. All or nothing: a `422` means none of the batch landed.

        **An adjustment is read when a payslip is calculated.** A `draft` payslip whose period
        holds `date` takes it in on its next calculation. An `approved` or `paid` one does not:
        it is recalculated only by hand in the web application, and nothing here tells you
        whether that happened. Check the payslip's status for the month before filing into it.

        **Send an `Idempotency-Key`.** An adjustment carries no key of yours, so a retry after a
        timeout files it a second time unless the header says it is the same attempt. The
        answer lists what was created, in the order sent.
        """
        return cast(
            PayrollSingleAdjustmentsCreateResponse,
            await self._transport.request(
                "POST",
                "/company/v3/payroll/single-adjustments",
                json=body,
                idempotency_key=idempotency_key,
            ),
        )

    async def delete(self, id: int) -> PayrollSingleAdjustmentsDeleteResponse:
        """Delete a single adjustment

        Deletes the adjustment. A payslip already calculated with it keeps the amount until it
        is calculated again — for an `approved` or `paid` one, only by hand in the web
        application.

        Another company's id is a `404`.
        """
        return cast(
            PayrollSingleAdjustmentsDeleteResponse,
            await self._transport.request(
                "DELETE",
                f"/company/v3/payroll/single-adjustments/{id}",
            ),
        )

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, users: list[int] | None = None, types: list[PayrollSingleAdjustmentsType] | None = None, date_from: str | None = None, date_to: str | None = None) -> PayrollSingleAdjustmentsListResponse:
        """List single adjustments

        One-off additions and deductions, oldest first, with who they are for and the day they
        are dated.

        `amount` is never negative: `type` says whether it is added or taken off, and whether
        before or after tax. `date_from` and `date_to` bound the day, inclusive.

        Rows filed in the web application are listed too, and may carry `13th_pay`, which is
        computed there rather than filed here.
        """
        return cast(
            PayrollSingleAdjustmentsListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/payroll/single-adjustments",
                query={"per_page": per_page, "cursor": cursor, "users": users, "types": types, "date_from": date_from, "date_to": date_to},
            ),
        )


class AsyncWebhooksDeliveries(_AsyncNamespace):
    """`clockster.webhooks.deliveries`."""

    async def get(self, id: int) -> WebhooksDeliveriesGetResponse:
        """Read one webhook delivery

        Answers with the payload, unlike the listing: one row is not a hundred employee records.
        """
        return cast(
            WebhooksDeliveriesGetResponse,
            await self._transport.request(
                "GET",
                f"/company/v3/webhooks/deliveries/{id}",
            ),
        )

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, webhooks: list[int] | None = None, events: list[WebhooksEvent] | None = None, successful: bool | None = None, pending: bool | None = None, since: str | None = None, include: list[WebhooksDeliveriesInclude] | None = None) -> WebhooksDeliveriesListResponse:
        """List webhook deliveries

        What was sent, and what came of it. **Newest first**, unlike every other listing here: a
        delivery log is read to learn what just happened.

        `state` is the field to branch on. `delivered` and `failed` are final; `pending` is
        neither — the event is waiting out its backoff and will be tried again. Reading
        `is_successful: false` as failure is the mistake the two stored flags invite.

        `payload` is behind `include=payload` and off by default: a page of a hundred deliveries
        is a hundred employee records, and a caller watching its integration's health has no use
        for them. Reading one delivery answers with it either way.

        `webhook_id` is null where the endpoint has since been removed.
        """
        return cast(
            WebhooksDeliveriesListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/webhooks/deliveries",
                query={"per_page": per_page, "cursor": cursor, "webhooks": webhooks, "events": events, "successful": successful, "pending": pending, "since": since, "include": include},
            ),
        )

    async def redeliver(self, id: int, *, idempotency_key: str | None = None) -> WebhooksDeliveriesRedeliverResponse:
        """Send a delivery again

        Queues the recorded event for another attempt, and answers once queued rather than once
        delivered.

        A repair tool, now that transient failures retry themselves: this is for the case where
        the receiver was fixed after we had already given up. What goes out is the event as it
        was recorded, so `occurred_at` may be long past — which is why the envelope states it.
        """
        return cast(
            WebhooksDeliveriesRedeliverResponse,
            await self._transport.request(
                "POST",
                f"/company/v3/webhooks/deliveries/{id}/redeliver",
                idempotency_key=idempotency_key,
            ),
        )


class AsyncWebhooksEvents(_AsyncNamespace):
    """`clockster.webhooks.events`."""

    async def list(self) -> WebhooksEventsListResponse:
        """List subscribable events

        Every event name an endpoint can subscribe to.

        Served as well as specified, so a caller can check at runtime that a name it stored is
        still one we send rather than discovering it on the next save.
        """
        return cast(
            WebhooksEventsListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/webhooks/events",
            ),
        )


class AsyncAttendance(_AsyncNamespace):
    """`clockster.attendance`."""

    async def list(self, *, date_from: str | None = None, date_to: str | None = None, per_page: int | None = None, cursor: str | None = None, users: list[int] | None = None, locations: list[int] | None = None, statuses: list[AttendanceStatus] | None = None, sources: list[AttendanceSource] | None = None, include: list[AttendanceInclude] | None = None) -> AttendanceListResponse:
        """List clock-ins

        Marks inside a window of days, oldest first.

        **The window is required and capped at 90 days.** This is the largest table in the
        product; an unbounded read of it has no plan that finishes. `date_from` and `date_to`
        are plain dates matched against the clock the mark was stamped with, not against an
        instant — a day means the same thing here as it does to the person who worked it.

        **`datetime` is the moment as it was recorded**, offset included — the stored wall clock
        read in the stored zone, never shifted anywhere else. It is one field because it is one
        fact: the wall clock is the value without its offset, and the zone is the offset. On the
        rare row whose zone cannot be read it comes back with no offset at all, which is how you
        see that the zone was not known.

        `status` is `in`, `out` or `break`, not the integer the column keeps.

        Late arrivals are the one thing to plan for: a device that was offline uploads what it
        recorded earlier, so a mark can appear inside a window you have already read. Re-read
        the last few days with overlap rather than paging strictly forward and never looking
        back.
        """
        return cast(
            AttendanceListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/attendance",
                query={"date_from": date_from, "date_to": date_to, "per_page": per_page, "cursor": cursor, "users": users, "locations": locations, "statuses": statuses, "sources": sources, "include": include},
            ),
        )

    async def record(self, body: AttendanceRecordBody) -> AttendanceRecordResponse:
        """Record attendance

        Marks recorded by something you run — a turnstile of your own, a kiosk, your app.

        **`datetime` carries its own offset and is the only place time is stated** — send
        `2026-08-10T09:03:00+05:00` and `09:03:00` goes on file with `+05:00` beside it. There
        is no separate timezone field, and the offset is not optional: the wall clock and the
        zone are read off that one value, so they cannot disagree. A mark may not be dated in the
        future, nor more than 24 hours back: older than that is history being rewritten, and
        lateness already computed against the day would move under it.

        `status` is `in`, `out` or `break`, and the answer echoes it back in those words, with
        the moment as the instant it was recorded at — the same shapes the listing answers with.

        **A mark already on file for the same person, moment and direction is not written
        again**, whether it repeats across two requests or inside one. There is no key you own
        on this resource, so no promise of idempotency is made in general — but a retried upload
        will not double somebody's day. The answer says `created` or `unchanged` per item, with
        the id either way.

        The shift a mark belongs to is worked out afterwards, so `shift_id` is yours to send
        only if you already know it.
        """
        return cast(
            AttendanceRecordResponse,
            await self._transport.request(
                "POST",
                "/company/v3/attendance",
                json=body,
            ),
        )


class AsyncDepartments(_AsyncNamespace):
    """`clockster.departments`."""

    async def delete(self, id: int) -> DepartmentsDeleteResponse:
        """Delete a department

        **Refused while anybody is in it** — 409, `department_in_use`.

        Once it goes, so do its managers, and there is no way to reconstruct who was in it.

        Move the people first, then delete. Somebody dismissed does not count as being in it.
        """
        return cast(
            DepartmentsDeleteResponse,
            await self._transport.request(
                "DELETE",
                f"/company/v3/departments/{id}",
            ),
        )

    async def get(self, id: int, *, include: list[DepartmentsInclude] | None = None) -> DepartmentsGetResponse:
        """Read one department

        The same keys and the same `include` vocabulary as the listing — `include=managers` adds the managers. Somebody else's id is a `404`.
        """
        return cast(
            DepartmentsGetResponse,
            await self._transport.request(
                "GET",
                f"/company/v3/departments/{id}",
                query={"include": include},
            ),
        )

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, search: str | None = None, updated_since: str | None = None, include: list[DepartmentsInclude] | None = None) -> DepartmentsListResponse:
        """List departments

        `include=managers` adds the managers. Without it the key is absent, never null standing in for "not asked for".
        """
        return cast(
            DepartmentsListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/departments",
                query={"per_page": per_page, "cursor": cursor, "search": search, "updated_since": updated_since, "include": include},
            ),
        )

    async def upsert(self, body: DepartmentsUpsertBody) -> DepartmentsUpsertResponse:
        """Create or update departments

        Up to 100 entries in one call, matched on `external_id`.

        **Not matched on the name.** Renaming an entry on your side updates ours, where matching
        on `title` would have created a second and orphaned the first.
        """
        return cast(
            DepartmentsUpsertResponse,
            await self._transport.request(
                "POST",
                "/company/v3/departments/upsert",
                json=body,
            ),
        )


class AsyncDocuments(_AsyncNamespace):
    """`clockster.documents`."""

    async def delete(self, id: int) -> DocumentsDeleteResponse:
        """Delete a document

        Deletes the document, its file records and the stored objects behind them.

        **A document everyone has signed cannot be deleted** — `409`, code `document_signed`.

        Another company's id is a `404`.
        """
        return cast(
            DocumentsDeleteResponse,
            await self._transport.request(
                "DELETE",
                f"/company/v3/documents/{id}",
            ),
        )

    async def get(self, id: int, *, include: list[DocumentsInclude] | None = None) -> DocumentsGetResponse:
        """Read one document

        The same keys the listing answers with, and the same `include` vocabulary. Another company's id is a `404`.
        """
        return cast(
            DocumentsGetResponse,
            await self._transport.request(
                "GET",
                f"/company/v3/documents/{id}",
                query={"include": include},
            ),
        )

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, party: DocumentsParty | None = None, external_ids: list[str] | None = None, users: list[int] | None = None, locations: list[int] | None = None, departments: list[int] | None = None, positions: list[int] | None = None, user_filters: list[int] | None = None, types: list[DocumentsType] | None = None, employment_types: list[DocumentsEmploymentType] | None = None, search: str | None = None, updated_since: str | None = None, expires_after: str | None = None, expires_before: str | None = None, effective_from: str | None = None, effective_to: str | None = None, include: list[DocumentsInclude] | None = None) -> DocumentsListResponse:
        """List documents

        The company's paperwork, oldest first, paged on a cursor.

        **Both kinds of document.** `party` is `employee` for a document about one of your
        people and `counterparty` for one a counterparty signs. Filter with `party=employee` or
        `party=counterparty`; leave it out for both.

        **`signature.state` is derived, because there is no column for it.** `none` when nobody
        has to sign, then `rejected`, `revoked`, `pending` in that order of precedence, and
        `signed` only when every signer has. Refusal outranks an outstanding signature, so a
        document one person refused reads `rejected` even while others are still pending.
        `completed_at` is set only for `signed`, and is when the last signer signed.

        **Dates are three shapes in one payload.** `start_date`, `end_date` and
        `expiration_date` are plain `YYYY-MM-DD` — they are date columns and carry no time or
        zone. `created_at` is an instant with an offset.

        `expires_after` and `expires_before` are a plain range of dates.

        `effective_from` and `effective_to` select documents valid during a window: a document
        starts on or before your `effective_to` and either has no end date or ends on or after
        your `effective_from`. Both are required together. **A document with no `start_date`
        never matches** — a row with no interval cannot overlap one.

        `locations`, `departments`, `positions` and `user_filters` all reach the document
        through the person it is about, so **a document with no `user_id` matches none of
        them**. The web app files company-level documents that way.

        **`updated_since` reads only what changed**, as an instant rather than a date so a
        caller polling every few minutes can say which minute. Two things it will not show you,
        and both are ours rather than yours: a document changed by a path inside the product
        that writes the row directly keeps its old timestamp, and so does one the back office
        modifies. Signature progress is the common case of the second — a signature completed
        through the web app does not move `updated_at`. Re-read with overlap if you depend on
        catching those.

        Documents the product files for its own machinery are never listed.
        """
        return cast(
            DocumentsListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/documents",
                query={"per_page": per_page, "cursor": cursor, "party": party, "external_ids": external_ids, "users": users, "locations": locations, "departments": departments, "positions": positions, "user_filters": user_filters, "types": types, "employment_types": employment_types, "search": search, "updated_since": updated_since, "expires_after": expires_after, "expires_before": expires_before, "effective_from": effective_from, "effective_to": effective_to, "include": include},
            ),
        )

    async def upsert(self, body: DocumentsUpsertBody) -> DocumentsUpsertResponse:
        """File documents

        Up to 100 documents in one call, matched on `external_id`, which is required here.

        **The bytes go up separately.** `POST /company/v3/files` takes one file and answers an
        id; send that as `file_id`. A file may be claimed once: one already hanging off a
        document is refused rather than moved.

        **An uploaded file waits to be claimed and is not cleaned up.** A batch refused at the
        hundredth document leaves all hundred files staged and still valid, so a retry should
        send the same `file_id`s rather than uploading them again.

        `parent_external_id` links a supplementary agreement to what it amends, by your key
        rather than ours. It resolves against documents already filed — not against another item
        of the same batch — and a key matching nothing clears the link rather than failing.

        `user_id` is required and may name somebody who has left: termination paperwork is filed
        after a dismissal, which is exactly when it is needed.

        **No signers.** Signing runs conversions and outbound calls that do not belong under a
        versioned contract, so documents filed here are always `party: employee`. Signature
        state is readable; creating a signing request is not offered yet.

        `author_id` is set to the subject: this token authenticates a company, not a person.
        """
        return cast(
            DocumentsUpsertResponse,
            await self._transport.request(
                "POST",
                "/company/v3/documents/upsert",
                json=body,
            ),
        )


class AsyncFiles(_AsyncNamespace):
    """`clockster.files`."""

    async def upload(self, file: bytes | IO[bytes], *, filename: str = "upload", name: str | None = None) -> FilesUploadResponse:
        """Upload a file

        One file, `multipart/form-data`, field name `file`. The only route on this surface that
        is not JSON.

        It answers an `id`. That id is what `POST /company/v3/documents/upsert` takes as
        `file_id`; until a document claims it the file belongs to nothing.

        Up to 10 MB. `pdf`, `doc`, `docx`, `xls`, `xlsx`, `jpg`, `jpeg`, `png` — the content is
        checked, not just the extension. `name` is optional and defaults to the uploaded
        filename without its extension.

        `url` is signed and short-lived: read it, do not store it. Read the document again to
        get a fresh one.
        """
        return cast(
            FilesUploadResponse,
            await self._transport.request(
                "POST",
                "/company/v3/files",
                files={"file": (filename, file)},
                data={"name": name},
            ),
        )


class AsyncLocations(_AsyncNamespace):
    """`clockster.locations`."""

    async def delete(self, id: int) -> LocationsDeleteResponse:
        """Delete a location

        **Refused while anybody works there** — 409, `location_in_use` — counting both the
        location on a person's record and the several they may also be assigned to.

        **Refused while anything sits beneath it** — 409, `location_has_children`. Deleting a
        parent detaches its whole subtree and destroys the rows describing the ancestry, and
        this API cannot express a hierarchy at all, so you would not be able to see what you
        had taken apart.

        Once it goes, so do its managers, its device assignments and any auto-scheduler
        configured for it; devices, schedules, tasks and approval routes keep working with the
        location set to null. None of that is recoverable and none of it is logged.

        Move the people first, then delete.
        """
        return cast(
            LocationsDeleteResponse,
            await self._transport.request(
                "DELETE",
                f"/company/v3/locations/{id}",
            ),
        )

    async def get(self, id: int, *, include: list[LocationsInclude] | None = None) -> LocationsGetResponse:
        """Read one location

        The same keys the listing answers with. Somebody else's id is a `404`, where asking the listing for it answers `200` with an empty array and leaves you counting.
        """
        return cast(
            LocationsGetResponse,
            await self._transport.request(
                "GET",
                f"/company/v3/locations/{id}",
                query={"include": include},
            ),
        )

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, search: str | None = None, include: list[LocationsInclude] | None = None, codes: list[str] | None = None, updated_since: str | None = None) -> LocationsListResponse:
        """List locations

        Ordered by `id` and paged on a cursor: no page number, no total, and nothing repeated
        or skipped while the list is written to. A cursor issued for another ordering is
        refused rather than silently restarting the list.

        Coordinates are numbers, and a latitude of exactly 0 is a coordinate rather than a
        missing one.

        `include=managers` adds the employees who manage the location, as on departments and
        user filters.
        """
        return cast(
            LocationsListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/locations",
                query={"per_page": per_page, "cursor": cursor, "search": search, "include": include, "codes": codes, "updated_since": updated_since},
            ),
        )

    async def upsert(self, body: LocationsUpsertBody) -> LocationsUpsertResponse:
        """Create or update locations

        Up to 100 entries in one call, matched on `external_id`.

        **Not matched on the name.** Renaming an entry on your side updates ours, where matching
        on `title` would have created a second and orphaned the first.

        `code` and `external_id` are different things and both are kept: `code` is a label you
        fill in and we never validate, `external_id` is what the match runs on. Coordinates and
        radius are set here too.
        """
        return cast(
            LocationsUpsertResponse,
            await self._transport.request(
                "POST",
                "/company/v3/locations/upsert",
                json=body,
            ),
        )


class AsyncPayroll(_AsyncNamespace):
    """`clockster.payroll`."""

    def __init__(self, transport: _AsyncTransport) -> None:
        super().__init__(transport)
        self.payslips = AsyncPayrollPayslips(transport)
        self.single_adjustments = AsyncPayrollSingleAdjustments(transport)


class AsyncPositions(_AsyncNamespace):
    """`clockster.positions`."""

    async def delete(self, id: int) -> PositionsDeleteResponse:
        """Delete a position

        **Refused while anybody holds it** — 409, `position_in_use`.

        Beyond the people: deleting a position destroys its auto-scheduler staffing
        configuration outright, so a rota that says "two bakers on nights" stops saying it.

        Move the people first, then delete.
        """
        return cast(
            PositionsDeleteResponse,
            await self._transport.request(
                "DELETE",
                f"/company/v3/positions/{id}",
            ),
        )

    async def get(self, id: int, *, include: list[str] | None = None) -> PositionsGetResponse:
        """Read one position

        The same keys the listing answers with. A position carries no managers, so asking to include them is refused rather than answered with an empty list.
        """
        return cast(
            PositionsGetResponse,
            await self._transport.request(
                "GET",
                f"/company/v3/positions/{id}",
                query={"include": include},
            ),
        )

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, search: str | None = None, updated_since: str | None = None, include: list[str] | None = None) -> PositionsListResponse:
        """List positions

        A position carries no managers, so asking to include them is refused rather than answered with an empty list.
        """
        return cast(
            PositionsListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/positions",
                query={"per_page": per_page, "cursor": cursor, "search": search, "updated_since": updated_since, "include": include},
            ),
        )

    async def upsert(self, body: PositionsUpsertBody) -> PositionsUpsertResponse:
        """Create or update positions

        Up to 100 entries in one call, matched on `external_id`.

        **Not matched on the name.** Renaming an entry on your side updates ours, where matching
        on `title` would have created a second and orphaned the first.
        """
        return cast(
            PositionsUpsertResponse,
            await self._transport.request(
                "POST",
                "/company/v3/positions/upsert",
                json=body,
            ),
        )


class AsyncSchedules(_AsyncNamespace):
    """`clockster.schedules`."""

    async def create(self, body: SchedulesCreateBody, *, idempotency_key: str | None = None) -> SchedulesCreateResponse:
        """Create schedules

        Up to 25 schedules in one call, each a kind of day, the days it falls on, and the people
        it is for. `type` is per item, so a rota and the absences inside it go together.

        There are no repeat patterns: send the dates. If you want every Monday, say which
        Mondays.

        **Send the rota as one call, not as twenty.** Everyone named is notified, once per call —
        so the same twenty schedules sent one at a time buzz in somebody's pocket twenty times.

        **This is the write to send an `Idempotency-Key` with.** A schedule carries no key of
        yours, so a retry after a timeout files the rota a second time unless the header tells us
        it is the same attempt.

        **Schedules carry no key you own**, so a resend duplicates rather than converges. A
        `422` means none of the batch landed and is safe to fix and send again; a timeout is
        not — read back before retrying. The answer lists what was created, in the order sent.

        **`type` decides what else is required.** `work` needs `timezone` and either
        `start`/`end` or `shifts`. `free` — a day with hours to make up rather than hours to
        keep — needs `timezone`, `start`, `end`, and takes `time_planned`. `leave` needs only
        `leave_type`.

        `start` and `end` are clock times, `HH:MM:SS`, read in `timezone` — not instants, whatever
        a generated client calls the field. `timezone` is a fixed offset, `+05:00` or `Z`.

        **The answer is not an echo of the request, so read it.** A day with two or more `shifts`
        takes its `start`, `end` and `time_planned` from them and comes back with `is_split`
        true. A day with exactly one shift is not a split day: the hours move onto the day itself
        and `shifts` comes back empty. `time_planned` for a worked day is always computed —
        the hours less the break — never taken from what you sent.

        **Every span is seconds**, `break_time` and `grace_start`/`grace_end` included. Grace is
        stored to the minute, so send a multiple of 60; the maximum is 3600.

        **Grace is not the same as a boundary.** It is how far past the start a person may arrive
        and still be credited from the shift boundary. How far outside the shift a punch is
        collected at all is a company setting and is not on this endpoint.

        There is no `title` — one is generated and it means nothing to you. One schedule takes up
        to 366 dates, 200 people and 8 shifts.
        """
        return cast(
            SchedulesCreateResponse,
            await self._transport.request(
                "POST",
                "/company/v3/schedules",
                json=body,
                idempotency_key=idempotency_key,
            ),
        )

    async def delete(self, id: int) -> SchedulesDeleteResponse:
        """Delete a schedule

        Everyone who was on it is notified, the same way a change to it would notify them.

        **A default schedule is refused** — 409, `schedule_is_default`. It is what the company
        falls back to.

        **An open shift is refused** — 409, `schedule_is_open`. Deleting one also removes its
        siblings and recomputes their days, which this API can neither create nor show you. Use
        the web application.
        """
        return cast(
            SchedulesDeleteResponse,
            await self._transport.request(
                "DELETE",
                f"/company/v3/schedules/{id}",
            ),
        )

    async def get(self, id: int) -> SchedulesGetResponse:
        """Read one schedule

        Exactly what creating it answered with — the same keys, the shifts and the people
        included, since those are the schedule rather than an optional extra.

        Worth reading back after a create: a day with two or more shifts takes its `start`,
        `end` and `time_planned` from them, and a day with exactly one has the shift folded into
        it and comes back with `shifts` empty.

        There is no listing of schedules. `GET /company/v3/timesheets` answers what a person is
        scheduled for on a day, which is the question a rota is usually asked.
        """
        return cast(
            SchedulesGetResponse,
            await self._transport.request(
                "GET",
                f"/company/v3/schedules/{id}",
            ),
        )


class AsyncTasks(_AsyncNamespace):
    """`clockster.tasks`."""

    async def get(self, id: int, *, include: list[TasksInclude] | None = None) -> TasksGetResponse:
        """Read one task

        The same keys the listing answers with, and the same `include` vocabulary. Another company's id is a `404`.
        """
        return cast(
            TasksGetResponse,
            await self._transport.request(
                "GET",
                f"/company/v3/tasks/{id}",
                query={"include": include},
            ),
        )

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, external_ids: list[str] | None = None, users: list[int] | None = None, categories: list[int] | None = None, statuses: list[TasksStatus] | None = None, active: bool | None = None, search: str | None = None, due_from: str | None = None, due_to: str | None = None, updated_since: str | None = None, include: list[TasksInclude] | None = None) -> TasksListResponse:
        """List tasks

        Work as we hold it: what was issued, what became of it, and how it measured up.

        `kpi_fact` against `kpi_plan`, plus `time_worked`, are the point of reading a task back
        — what was asked for, what was achieved, how long it took. `status` says where it got
        to.

        **Twenty-four fields, not the forty the table has.** Eight of the rest configure how the
        mobile application behaves while the job is done — whether it demands a photo, records a
        location, keeps the steps in order. That is a task template's business, and neither
        useful nor settable here.

        `include=items` adds the steps, `include=managers` the people who approve or are
        notified. Without them the keys are absent, never null standing in for "not asked for".

        **`updated_since` is what an export should page on**, as an instant: a task moves
        through its statuses inside a working day, so a caller polling for completions needs to
        say which minute.

        `statuses` takes `created`, `started`, `paused`, `completed`, `incompleted` and
        `pastdue`. Three more exist in the database and none is offered: `finished` and
        `unfinished` are deprecated spellings, and `pending` is reached only through approval.
        A value that cannot be explained is worse than one that is absent.

        **Oldest first.** A first call lands on the earliest task this company ever issued,
        which for a long-standing one is years back. That order is what lets a full export
        finish in one walk, and it is not what you want for "what happened lately": ask with
        `updated_since`, or narrow with `due_from` and `due_to`.
        """
        return cast(
            TasksListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/tasks",
                query={"per_page": per_page, "cursor": cursor, "external_ids": external_ids, "users": users, "categories": categories, "statuses": statuses, "active": active, "search": search, "due_from": due_from, "due_to": due_to, "updated_since": updated_since, "include": include},
            ),
        )

    async def upsert(self, body: TasksUpsertBody) -> TasksUpsertResponse:
        """Issue tasks

        Up to 100 pieces of work in one call, matched on `external_id`, which is required here
        — a task has no natural key of its own, since the same round is issued every week under
        the same title.

        **`status` is not accepted, and neither are the timestamps around it.** The product
        moves a task through its lifecycle with events — completing notifies, approval routes,
        reopening makes it pastdue again — and a status written straight onto the row fires none
        of that. Issue the work here; read where it got to with `GET /company/v3/tasks`.

        **Eight fields are not accepted either** — `req_photo`, `req_sequence`, `gallery`,
        `get_location`, `get_timing`, `is_keep_status`, `req_approve`, `req_notify`. They
        configure the mobile application, not the job.

        **Where the work sits is taken from whoever it is for.** Omit `location_id`,
        `department_id` and `position_id` and they come from the assignee — your system knows
        the person, not our org chart. Send them to override.

        **`items` is an exception to the omitted-field rule**: sending it replaces the steps outright, because a step carries no key
        to match an incoming one against — and replacing them discards the completion the person
        doing the work recorded. Omit the key to leave them alone. `managers` likewise states
        who approves now rather than adding to them.

        `kpi_plan` has no "unset" — the column is NOT NULL with a default of 0, so an omitted
        plan is a plan of zero.
        """
        return cast(
            TasksUpsertResponse,
            await self._transport.request(
                "POST",
                "/company/v3/tasks/upsert",
                json=body,
            ),
        )


class AsyncTimesheets(_AsyncNamespace):
    """`clockster.timesheets`."""

    async def list(self, *, date_from: str | None = None, date_to: str | None = None, cursor: str | None = None, users: list[int] | None = None, locations: list[int] | None = None, departments: list[int] | None = None, positions: list[int] | None = None, employment: str | None = None, include: list[TimesheetsInclude] | None = None) -> TimesheetsListResponse:
        """Timesheets

        One row per person per calendar day of the window: what was planned, and — when asked
        for — what happened and how the two differ.

        **`planned` alone is the timesheet grid** — who was meant to work, when, and what kind
        of day it was. `include=actual` adds what was recorded, `include=variance` adds the
        difference. Either one is what makes the request expensive, because both require
        matching the clock-ins.

        **The four variance numbers are not additive.** Arriving three minutes late produces
        `time_late` 180 and `time_underworked` 180 — the same minutes, counted once as lateness
        and once as unfilled plan. Summing them double-counts.

        **`planned: null` means no schedule at all for that day.** It is rarer than it sounds: a
        company created with default settings carries a work and a leave schedule covering four
        years, so ordinary days off arrive as `type: leave` rather than as an absent plan. A day
        that was scheduled and not worked is the other case — a plan, an empty `actual`, and
        `time_underworked` equal to the whole planned time.

        **There is no `per_page`.** How many rows fifty people produce depends on the window and
        on who is scheduled, which the caller cannot predict and we can: the page is sized to a
        row budget instead, and `meta.users_per_page` reports what that came to. Paging walks
        people, so one person's whole period always arrives on a single page and a monthly total
        never has to be assembled across two.

        Holidays are not marked: take them from your own calendar. Drafts are never returned.
        """
        return cast(
            TimesheetsListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/timesheets",
                query={"date_from": date_from, "date_to": date_to, "cursor": cursor, "users": users, "locations": locations, "departments": departments, "positions": positions, "employment": employment, "include": include},
            ),
        )


class AsyncUserFilters(_AsyncNamespace):
    """`clockster.user_filters`."""

    async def delete(self, id: int) -> UserFiltersDeleteResponse:
        """Delete a user filter

        Members do not block it — a filter is a label, and a caller who keeps their filters in
        step re-creates it on the next sync.

        **Refused while an approval route points at it** — 409, `user_filter_in_use`. The route
        would survive with nobody to approve through it and quietly stop routing. Change the
        route first.
        """
        return cast(
            UserFiltersDeleteResponse,
            await self._transport.request(
                "DELETE",
                f"/company/v3/user-filters/{id}",
            ),
        )

    async def get(self, id: int, *, include: list[UserFiltersInclude] | None = None) -> UserFiltersGetResponse:
        """Read one user filter

        The same keys and the same `include` vocabulary as the listing. Somebody else's id is a `404`.
        """
        return cast(
            UserFiltersGetResponse,
            await self._transport.request(
                "GET",
                f"/company/v3/user-filters/{id}",
                query={"include": include},
            ),
        )

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, search: str | None = None, updated_since: str | None = None, include: list[UserFiltersInclude] | None = None) -> UserFiltersListResponse:
        """List user filters

        `include=managers` adds the managers, as on departments.
        """
        return cast(
            UserFiltersListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/user-filters",
                query={"per_page": per_page, "cursor": cursor, "search": search, "updated_since": updated_since, "include": include},
            ),
        )

    async def upsert(self, body: UserFiltersUpsertBody) -> UserFiltersUpsertResponse:
        """Create or update user filters

        Up to 100 entries in one call, matched on `external_id`.

        **Not matched on the name.** Renaming an entry on your side updates ours, where matching
        on `title` would have created a second and orphaned the first.
        """
        return cast(
            UserFiltersUpsertResponse,
            await self._transport.request(
                "POST",
                "/company/v3/user-filters/upsert",
                json=body,
            ),
        )


class AsyncUserRequests(_AsyncNamespace):
    """`clockster.user_requests`."""

    async def get(self, id: int) -> UserRequestsGetResponse:
        """Read one request

        Answers with `content`, unlike the listing: one row is one shape to make sense of, not a hundred.
        """
        return cast(
            UserRequestsGetResponse,
            await self._transport.request(
                "GET",
                f"/company/v3/user-requests/{id}",
            ),
        )

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, types: list[UserRequestsType] | None = None, statuses: list[UserRequestsStatus] | None = None, subtypes: list[str] | None = None, users: list[int] | None = None, updated_since: str | None = None, include: list[UserRequestsInclude] | None = None) -> UserRequestsListResponse:
        """List requests

        What people asked for, and what became of it — leave, schedule changes, corrections and
        money.

        **Read this to learn that a timesheet moved.** Half of everything here is a batch
        clock-in correction: somebody forgot to punch, a manager approved the fix, and the
        attendance for those days changed after the fact. Only 48 per cent of those are approved
        within three days of the day they correct, and a third reach back more than a week — so
        a caller that pulled a timesheet last week cannot assume it still holds. Attendance
        carries no timestamps of its own, which makes this listing paged on `updated_since` the
        only signal that anything has moved.

        `period` is the field that makes that usable: the span of days a request concerns,
        wherever its kind happens to keep them. A clock-in correction keeps them inside the
        punches, a leave request as a period or a list, a request for a certificate not at all —
        both ends are null there rather than invented.

        `subtype` is the second half of `type`, and the product keeps it in two different places
        — `content.type` for most kinds, `content.leave_type` for leave. It is answered as one
        field, and `subtypes` filters on both.

        `comment` is what the author wrote when filing it, ordinarily the reason. Comments the
        workflow writes itself — on acknowledgement, or when a spawned task closes — are not
        answered here.

        **Oldest first.** A first call lands on the earliest request this company ever filed,
        which for a long-standing one is years back. That order is what lets a full export
        finish in one walk, and it is not what you want for "what changed lately": ask with
        `updated_since`.

        `content` is behind `include=content`: its shape depends on the kind, and one schema
        describes one shape everywhere else on this surface.

        **Reading only.** Creating a request enters a workflow — approval routes resolve,
        approvers are notified, tasks are spawned — and approving one is a person's decision that
        a dismissal application or a sick note gives weight to.
        """
        return cast(
            UserRequestsListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/user-requests",
                query={"per_page": per_page, "cursor": cursor, "types": types, "statuses": statuses, "subtypes": subtypes, "users": users, "updated_since": updated_since, "include": include},
            ),
        )


class AsyncUsers(_AsyncNamespace):
    """`clockster.users`."""

    async def dismiss(self, body: UsersDismissBody) -> UsersDismissResponse:
        """Dismiss employees

        Up to 100 people in one call, each named by `external_id` or by `id`, exactly one per
        item.

        **This is dismissal, not erasure.** The record stays and stays readable: the person
        appears under `status=dismissed` with `dismissed_at` set, and the seat is freed for
        somebody else. It is the shape leaving actually has — a nightly sync noticing that
        twelve people are no longer on the roster.

        **There is no hard delete on this API.** Erasing a person takes their attendance,
        payroll, documents and bank details with them, with no way to undo it, and one ability
        grants this whole API — an integrator that syncs your roster cannot be given that
        without also being given erasure. If a retention obligation needs it, ask us.

        **Somebody already gone answers `already_dismissed`** rather than failing, which matters
        here because dismissing frees the key for a new hire.

        **If a key is held by two people** — one who left and one hired since — the living one
        is the one dismissed.

        What happens that you cannot see, and cannot undo:

        - Their sessions end immediately and their phone is unpaired.
        - Every terminal at their locations is told to forget their face. That is sent once and
          not retried, so a terminal that is offline at the time keeps admitting them.
        - **Requests still waiting on them to approve are cancelled**, not just their own. Dismiss
          a manager and their team's pending vacation requests are cancelled with them.
        - An offboarding process starts, if the company has one configured.
        - `date_leave` is filled in with today's date if it was empty.
        """
        return cast(
            UsersDismissResponse,
            await self._transport.request(
                "POST",
                "/company/v3/users/dismiss",
                json=body,
            ),
        )

    async def get(self, id: int, *, include: list[UsersInclude] | None = None) -> UsersGetResponse:
        """Read one employee

        One employee by our id. Prefer it over `?ids=` when you expect exactly one: someone who
        is not yours answers `404`, where the listing answers `200` with an empty array, so a
        status can be branched on without counting.

        Reachable for a dismissed person too.
        """
        return cast(
            UsersGetResponse,
            await self._transport.request(
                "GET",
                f"/company/v3/users/{id}",
                query={"include": include},
            ),
        )

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, search: str | None = None, updated_since: str | None = None, status: UsersStatus | None = None, ids: list[int] | None = None, codes: list[str] | None = None, external_ids: list[str] | None = None, locations: list[int] | None = None, departments: list[int] | None = None, positions: list[int] | None = None, user_filters: list[int] | None = None, employment: list[UsersEmployment] | None = None, include: list[UsersInclude] | None = None) -> UsersListResponse:
        """List employees

        The roster as we hold it. Every scalar is always present; a relation appears only when
        `include` names it.

        **`status` decides whether the people who left are in the answer** — `active` by
        default, `dismissed` for only them, `all` for both. A dismissed employee keeps their
        record: `date_leave` says when they were let go and `dismissed_at` when the record was
        closed. A sync that never asks for them cannot learn that anyone left, so ask
        periodically even if your day-to-day reads are `active`.

        **`external_ids` is the other half of the roster write.** Ask with the same keys you
        sent to `/users/upsert` and reconcile without keeping a map of our ids.

        `updated_since` reads only what changed, against the `updated_at` every row carries.
        """
        return cast(
            UsersListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/users",
                query={"per_page": per_page, "cursor": cursor, "search": search, "updated_since": updated_since, "status": status, "ids": ids, "codes": codes, "external_ids": external_ids, "locations": locations, "departments": departments, "positions": positions, "user_filters": user_filters, "employment": employment, "include": include},
            ),
        )

    async def upsert(self, body: UsersUpsertBody) -> UsersUpsertResponse:
        """Create or update employees

        The roster, written in batches of up to 100. `external_id` is optional here and behaves
        as it does everywhere: an item carrying one updates the person it names, an item without
        one always creates. `first_name`, `role` and `location_id` are the minimum.

        The field set is what an HR system holds about an employee.

        A person created here reaches the turnstiles of their location, and every location's
        devices are told once for the whole batch rather than once per person.
        """
        return cast(
            UsersUpsertResponse,
            await self._transport.request(
                "POST",
                "/company/v3/users/upsert",
                json=body,
            ),
        )


class AsyncWebhooks(_AsyncNamespace):
    """`clockster.webhooks`."""

    def __init__(self, transport: _AsyncTransport) -> None:
        super().__init__(transport)
        self.deliveries = AsyncWebhooksDeliveries(transport)
        self.events = AsyncWebhooksEvents(transport)

    async def create(self, body: WebhooksCreateBody, *, idempotency_key: str | None = None) -> WebhooksCreateResponse:
        """Create a webhook endpoint

        Connect an endpoint. Answers 201 with the signing secret it will use.

        **No `external_id`, and no upsert**, unlike every other write on this surface. Those
        mirror something your system already holds and must match on its own key; an endpoint is
        created here and its identity is ours, so there is nothing to match against.

        The secret is generated, never accepted: a caller-chosen signing key is a caller-chosen
        weakness. Replace it with `POST /company/v3/webhooks/{id}/secret`.

        Deliveries carry `X-Clockster-Event`, `X-Clockster-Delivery` (constant across retries,
        so a repeat can be recognised), `X-Clockster-Timestamp` and `X-Clockster-Signature` —
        `sha256=` HMAC-SHA256 of `timestamp + "." + rawBody` under the secret. The body is
        `{"id", "event", "occurred_at", "data"}`.
        """
        return cast(
            WebhooksCreateResponse,
            await self._transport.request(
                "POST",
                "/company/v3/webhooks",
                json=body,
                idempotency_key=idempotency_key,
            ),
        )

    async def delete(self, id: int) -> WebhooksDeleteResponse:
        """Delete a webhook endpoint

        Removes the endpoint. What was delivered to it stays readable: the delivery's link is
        nulled rather than cascaded, because the record of what was sent is the company's.
        """
        return cast(
            WebhooksDeleteResponse,
            await self._transport.request(
                "DELETE",
                f"/company/v3/webhooks/{id}",
            ),
        )

    async def get(self, id: int) -> WebhooksGetResponse:
        """Read one webhook endpoint
        """
        return cast(
            WebhooksGetResponse,
            await self._transport.request(
                "GET",
                f"/company/v3/webhooks/{id}",
            ),
        )

    async def list(self, *, per_page: int | None = None, cursor: str | None = None, active: bool | None = None) -> WebhooksListResponse:
        """List webhook endpoints

        The endpoints this company has connected, and the health of each.

        `health` answers what `active` cannot: whether a person switched an endpoint off or a
        run of failures did. Five consecutive permanent failures — a wrong address, refused
        credentials — switch it off, as do twenty transient ones. `disabled_reason` says which.

        `secret` is answered in full because verifying a signature is impossible without it.
        The credential we authenticate to the receiver *with* is not: `auth` names the scheme
        and, for basic, the username, and never the password or bearer token.
        """
        return cast(
            WebhooksListResponse,
            await self._transport.request(
                "GET",
                "/company/v3/webhooks",
                query={"per_page": per_page, "cursor": cursor, "active": active},
            ),
        )

    async def rotate_secret(self, id: int, *, idempotency_key: str | None = None) -> WebhooksRotateSecretResponse:
        """Replace the signing secret

        Answers the endpoint with a new secret.

        **Send an `Idempotency-Key`.** The secret is shown once, so a retry after a lost
        response would rotate a second time and leave you holding one that signs nothing — with
        the header, the retry is answered with the secret the first call minted.

        Deliveries already queued are signed with whichever secret is current when they are
        actually sent, so accept both for as long as your backlog can be deep — up to about a
        day where transient failures are being retried.
        """
        return cast(
            WebhooksRotateSecretResponse,
            await self._transport.request(
                "POST",
                f"/company/v3/webhooks/{id}/secret",
                idempotency_key=idempotency_key,
            ),
        )

    async def update(self, id: int, body: WebhooksUpdateBody) -> WebhooksUpdateResponse:
        """Replace a webhook endpoint

        Replaces rather than patches: half a subscription is not a state worth reaching by
        accident.

        Saving clears the failure tally and any automatic switch-off — you are saying something
        changed, so what the history counted no longer describes what is there. This is how an
        endpoint switched off by repeated failures is put back into service.
        """
        return cast(
            WebhooksUpdateResponse,
            await self._transport.request(
                "PUT",
                f"/company/v3/webhooks/{id}",
                json=body,
            ),
        )


class _AsyncClocksterApi(_AsyncNamespace):
    def __init__(self, transport: _AsyncTransport) -> None:
        super().__init__(transport)
        self.attendance = AsyncAttendance(transport)
        self.departments = AsyncDepartments(transport)
        self.documents = AsyncDocuments(transport)
        self.files = AsyncFiles(transport)
        self.locations = AsyncLocations(transport)
        self.payroll = AsyncPayroll(transport)
        self.positions = AsyncPositions(transport)
        self.schedules = AsyncSchedules(transport)
        self.tasks = AsyncTasks(transport)
        self.timesheets = AsyncTimesheets(transport)
        self.user_filters = AsyncUserFilters(transport)
        self.user_requests = AsyncUserRequests(transport)
        self.users = AsyncUsers(transport)
        self.webhooks = AsyncWebhooks(transport)

    async def me(self) -> MeResponse:
        """Whose token this is

        Confirms which company a key belongs to.

        Answers the id and the name, and nothing else: everything a key opens is reachable from
        the endpoints themselves, and a company attribute this surface does not act on would
        only read as one it does.
        """
        return cast(
            MeResponse,
            await self._transport.request(
                "GET",
                "/company/v3/me",
            ),
        )
