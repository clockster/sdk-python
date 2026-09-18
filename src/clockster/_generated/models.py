"""Every shape the Company API answers with or accepts, as TypedDicts.

Generated from openapi/company-v3.json — see scripts/generate.py. A key the document marks optional
is `NotRequired`, which is what an `include` relation is: absent unless it was asked for, never null
because it was not.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    # 3.11 has it in `typing`; the annotations here are strings either way, so this import runs in
    # no interpreter and the package keeps its single dependency.
    from typing_extensions import NotRequired

__all__ = [
    "AttendanceInclude",
    "AttendanceListResponse",
    "AttendanceListRow",
    "AttendanceListRowAttachment",
    "AttendanceListRowLocation",
    "AttendanceRecordAttendanceItem",
    "AttendanceRecordBody",
    "AttendanceRecordResponse",
    "AttendanceRecordRow",
    "AttendanceSource",
    "AttendanceStatus",
    "DeleteOutcome",
    "DepartmentsDeleteResponse",
    "DepartmentsGetData",
    "DepartmentsGetResponse",
    "DepartmentsInclude",
    "DepartmentsListResponse",
    "DepartmentsListRow",
    "DepartmentsUpsertBody",
    "DepartmentsUpsertItem",
    "DepartmentsUpsertResponse",
    "DocumentsDeleteResponse",
    "DocumentsEmploymentType",
    "DocumentsGetData",
    "DocumentsGetDataAttachment",
    "DocumentsGetDataLaborContract",
    "DocumentsGetDataSignature",
    "DocumentsGetDataSigner",
    "DocumentsGetResponse",
    "DocumentsInclude",
    "DocumentsListResponse",
    "DocumentsListRow",
    "DocumentsListRowAttachment",
    "DocumentsListRowLaborContract",
    "DocumentsListRowSignature",
    "DocumentsListRowSigner",
    "DocumentsParty",
    "DocumentsType",
    "DocumentsUpsertBody",
    "DocumentsUpsertDocument",
    "DocumentsUpsertResponse",
    "EmployeeShort",
    "FilesUploadData",
    "FilesUploadResponse",
    "FreeSchedule",
    "LeaveSchedule",
    "LocationsDeleteResponse",
    "LocationsGetData",
    "LocationsGetResponse",
    "LocationsInclude",
    "LocationsListResponse",
    "LocationsListRow",
    "LocationsUpsertBody",
    "LocationsUpsertItem",
    "LocationsUpsertResponse",
    "MeData",
    "MeResponse",
    "PageLinks",
    "PageMeta",
    "PayrollPayslipsListMeta",
    "PayrollPayslipsListResponse",
    "PayrollPayslipsListRow",
    "PayrollPayslipsListRowAddition",
    "PayrollPayslipsListRowDeduction",
    "PayrollPayslipsListRowPeriod",
    "PayrollPayslipsListRowSalary",
    "PayrollPayslipsListRowUser",
    "PayrollPayslipsStatus",
    "PositionsDeleteResponse",
    "PositionsGetData",
    "PositionsGetResponse",
    "PositionsListResponse",
    "PositionsListRow",
    "PositionsUpsertBody",
    "PositionsUpsertItem",
    "PositionsUpsertResponse",
    "Refusal",
    "RefusalError",
    "SchedulesCreateBody",
    "SchedulesCreateResponse",
    "SchedulesCreateRow",
    "SchedulesCreateRowShift",
    "SchedulesCreateRowUser",
    "SchedulesDeleteResponse",
    "SchedulesGetData",
    "SchedulesGetDataShift",
    "SchedulesGetDataUser",
    "SchedulesGetResponse",
    "SchedulesLeaveType",
    "SchedulesType",
    "TasksGetData",
    "TasksGetDataItem",
    "TasksGetResponse",
    "TasksInclude",
    "TasksListMeta",
    "TasksListResponse",
    "TasksListRow",
    "TasksListRowItem",
    "TasksPriority",
    "TasksStatus",
    "TasksUpsertBody",
    "TasksUpsertResponse",
    "TasksUpsertTask",
    "TasksUpsertTaskItem",
    "TimesheetsInclude",
    "TimesheetsListMeta",
    "TimesheetsListResponse",
    "TimesheetsListRow",
    "TimesheetsListRowActual",
    "TimesheetsListRowActualShift",
    "TimesheetsListRowPlanned",
    "TimesheetsListRowPlannedShift",
    "TimesheetsListRowPlannedShiftLocation",
    "TimesheetsListRowUser",
    "TimesheetsListRowVariance",
    "UpsertOutcome",
    "UserFiltersDeleteResponse",
    "UserFiltersGetData",
    "UserFiltersGetResponse",
    "UserFiltersInclude",
    "UserFiltersListResponse",
    "UserFiltersListRow",
    "UserFiltersUpsertBody",
    "UserFiltersUpsertItem",
    "UserFiltersUpsertResponse",
    "UserRequestsGetData",
    "UserRequestsGetDataContent",
    "UserRequestsGetDataContentClockin",
    "UserRequestsGetDataPeriod",
    "UserRequestsGetResponse",
    "UserRequestsInclude",
    "UserRequestsListResponse",
    "UserRequestsListRow",
    "UserRequestsListRowContent",
    "UserRequestsListRowContentClockin",
    "UserRequestsListRowPeriod",
    "UserRequestsStatus",
    "UserRequestsType",
    "UsersDismissBody",
    "UsersDismissResponse",
    "UsersDismissUser",
    "UsersEmployment",
    "UsersGender",
    "UsersGetData",
    "UsersGetDataDepartment",
    "UsersGetDataDismissal",
    "UsersGetDataLocation",
    "UsersGetDataMeta",
    "UsersGetResponse",
    "UsersInclude",
    "UsersListResponse",
    "UsersListRow",
    "UsersListRowDepartment",
    "UsersListRowDismissal",
    "UsersListRowLocation",
    "UsersListRowMeta",
    "UsersLocale",
    "UsersRole",
    "UsersStatus",
    "UsersUpsertBody",
    "UsersUpsertResponse",
    "UsersUpsertUser",
    "ValidationRefusal",
    "ValidationRefusalError",
    "WebhooksCreateAuthBasic",
    "WebhooksCreateBody",
    "WebhooksCreateData",
    "WebhooksCreateDataAuth",
    "WebhooksCreateDataHealth",
    "WebhooksCreateResponse",
    "WebhooksDeleteResponse",
    "WebhooksDeliveriesGetData",
    "WebhooksDeliveriesGetDataPayload",
    "WebhooksDeliveriesGetResponse",
    "WebhooksDeliveriesInclude",
    "WebhooksDeliveriesListResponse",
    "WebhooksDeliveriesListRow",
    "WebhooksDeliveriesListRowPayload",
    "WebhooksDeliveriesRedeliverResponse",
    "WebhooksEvent",
    "WebhooksEventsListResponse",
    "WebhooksGetData",
    "WebhooksGetDataAuth",
    "WebhooksGetDataHealth",
    "WebhooksGetResponse",
    "WebhooksListResponse",
    "WebhooksListRow",
    "WebhooksListRowAuth",
    "WebhooksListRowHealth",
    "WebhooksRotateSecretData",
    "WebhooksRotateSecretDataAuth",
    "WebhooksRotateSecretDataHealth",
    "WebhooksRotateSecretResponse",
    "WebhooksUpdateAuthBasic",
    "WebhooksUpdateBody",
    "WebhooksUpdateData",
    "WebhooksUpdateDataAuth",
    "WebhooksUpdateDataHealth",
    "WebhooksUpdateResponse",
    "WorkSchedule",
    "WorkScheduleShift",
]


AttendanceInclude = Literal["user", "location", "attachments"]

AttendanceSource = Literal["device", "mobile", "frontend", "api", "system"]

AttendanceStatus = Literal["out", "in", "break"]

DepartmentsInclude = Literal["managers"]

DocumentsEmploymentType = Literal["full_time", "part_time", "irregular_hours", "contract_1", "contract_2", "apprenticeship", "traineeship", "piece_rate", "probation", "outstaffing"]

DocumentsInclude = Literal["attachments", "signers", "labor_contract"]

DocumentsParty = Literal["employee", "counterparty"]

DocumentsType = Literal["passport", "cv", "diploma", "medical", "photo", "other", "medical_book", "employment_agreement", "termination_of_employment_agreement", "equipment_agreement", "application", "order", "supplementary_agreement", "job_description", "nda", "non_compete_agreement", "data_processing_agreement", "act_of_service_acceptance", "health_and_safety_briefing", "shift_schedule", "letter", "vacation_schedule", "contract", "agreement", "goods_release_note", "reconciliation_act", "return_to_supplier", "driver_license", "birth_certificate", "marriage_certificate", "divorce_certificate", "change_fio_certificate"]

LocationsInclude = Literal["managers"]

PayrollPayslipsStatus = Literal["draft", "approved", "paid"]

SchedulesLeaveType = Literal["annual", "unpaid", "sick", "unpaid_sick", "maternity", "paternity", "special", "day_off", "compensatory", "personal", "emergency", "unexcused_absence"]

SchedulesType = Literal["work", "free", "leave"]

TasksInclude = Literal["items", "managers", "user", "author"]

TasksPriority = Literal[0, 1]

TasksStatus = Literal["created", "started", "paused", "completed", "incompleted", "pastdue"]

TimesheetsInclude = Literal["actual", "variance", "user", "location", "department", "position"]

UserFiltersInclude = Literal["managers"]

UserRequestsInclude = Literal["content", "user", "author"]

UserRequestsStatus = Literal["pending", "accepted", "rejected", "cancelled", "approval", "execution", "signing"]

UserRequestsType = Literal["leave", "work", "general", "finance"]

UsersEmployment = Literal["full_time", "part_time", "irregular_hours", "contract_1", "contract_2", "apprenticeship", "traineeship", "piece_rate", "probation", "outstaffing"]

UsersGender = Literal["male", "female", "other"]

UsersInclude = Literal["location", "locations", "department", "position", "user_filters", "dismissal", "meta"]

UsersLocale = Literal["en", "ru", "kk", "uk", "id", "uz", "az", "fr", "vi", "zh"]

UsersRole = Literal["admin", "employee"]

UsersStatus = Literal["active", "dismissed", "all"]

WebhooksDeliveriesInclude = Literal["payload"]

WebhooksEvent = Literal["user.created", "user.updated", "user.deleted", "user.restored", "user.purged", "location.created", "location.updated", "location.deleted", "department.created", "department.updated", "department.deleted", "position.created", "position.updated", "position.deleted", "task.created", "task.completed", "task.approved", "task.rejected", "task.deleted"]

class WorkSchedule(TypedDict):
    # Which kind of day this is, and with it what else the item requires.
    type: SchedulesType
    # The days this applies to, each `YYYY-MM-DD`. No repeats.
    dates: list[str]
    # Who the day is for, by id. At least one, and no repeats.
    users: list[int]
    # The location this is filed against, by id. Null clears it.
    location_id: NotRequired[int | None]
    # The department this is filed against, by id. Null clears it.
    department_id: NotRequired[int | None]
    # The position this is filed against, by id. Null clears it.
    position_id: NotRequired[int | None]
    # The UTC offset the clock times beside it are read in — `Z`, or `+05:00`. An offset rather than
    # a zone name, so the day is fixed to a moment rather than to a rule that may be changed later.
    timezone: str
    # When it starts, as a clock time `HH:MM:SS`, read in the offset beside it.
    start: NotRequired[str | None]
    # When it ends, as a clock time `HH:MM:SS`, read in the offset beside it.
    end: NotRequired[str | None]
    # Unpaid break within the day, in seconds.
    break_time: NotRequired[int | None]
    # How late an arrival still counts as on time, in seconds.
    grace_start: NotRequired[int | None]
    # How early a departure still counts as a full day, in seconds.
    grace_end: NotRequired[int | None]
    # Split the day into shifts instead of one span. Each carries its own clock times and may sit
    # somewhere other than the day does.
    shifts: NotRequired[list[WorkScheduleShift] | None]

class WorkScheduleShift(TypedDict):
    # When it starts, as a clock time `HH:MM:SS`, read in the offset beside it.
    start: str
    # When it ends, as a clock time `HH:MM:SS`, read in the offset beside it.
    end: str
    # The location this is filed against, by id. Null clears it.
    location_id: NotRequired[int | None]
    # The department this is filed against, by id. Null clears it.
    department_id: NotRequired[int | None]
    # The position this is filed against, by id. Null clears it.
    position_id: NotRequired[int | None]

class FreeSchedule(TypedDict):
    # Which kind of day this is, and with it what else the item requires.
    type: SchedulesType
    # The days this applies to, each `YYYY-MM-DD`. No repeats.
    dates: list[str]
    # Who the day is for, by id. At least one, and no repeats.
    users: list[int]
    # The location this is filed against, by id. Null clears it.
    location_id: NotRequired[int | None]
    # The department this is filed against, by id. Null clears it.
    department_id: NotRequired[int | None]
    # The position this is filed against, by id. Null clears it.
    position_id: NotRequired[int | None]
    # The UTC offset the clock times beside it are read in — `Z`, or `+05:00`. An offset rather than
    # a zone name, so the day is fixed to a moment rather than to a rule that may be changed later.
    timezone: str
    # When it starts, as a clock time `HH:MM:SS`, read in the offset beside it.
    start: str
    # When it ends, as a clock time `HH:MM:SS`, read in the offset beside it.
    end: str
    # How long the person is expected to work that day, in seconds.
    time_planned: NotRequired[int | None]

class LeaveSchedule(TypedDict):
    # Which kind of day this is, and with it what else the item requires.
    type: SchedulesType
    # The days this applies to, each `YYYY-MM-DD`. No repeats.
    dates: list[str]
    # Who the day is for, by id. At least one, and no repeats.
    users: list[int]
    # The location this is filed against, by id. Null clears it.
    location_id: NotRequired[int | None]
    # The department this is filed against, by id. Null clears it.
    department_id: NotRequired[int | None]
    # The position this is filed against, by id. Null clears it.
    position_id: NotRequired[int | None]
    # What kind of leave the day is.
    leave_type: SchedulesLeaveType

class Refusal(TypedDict):
    error: RefusalError

class RefusalError(TypedDict):
    code: str
    message: str
    request_id: str

class ValidationRefusal(TypedDict):
    error: ValidationRefusalError

class ValidationRefusalError(TypedDict):
    code: str
    message: str
    request_id: str
    errors: dict[str, list[str]]

class PageLinks(TypedDict):
    first: None
    last: None
    prev: str | None
    next: str | None

class PageMeta(TypedDict):
    path: str
    per_page: int
    next_cursor: str | None
    prev_cursor: str | None

class EmployeeShort(TypedDict):
    id: int
    external_id: str | None
    code: str | None
    first_name: str
    middle_name: str | None
    last_name: str

class UpsertOutcome(TypedDict):
    external_id: str | None
    id: int
    result: str

class DeleteOutcome(TypedDict):
    id: int
    result: str

class AttendanceListResponse(TypedDict):
    data: list[AttendanceListRow]
    links: PageLinks
    meta: PageMeta

class AttendanceListRow(TypedDict):
    id: int
    user_id: int
    location_id: int | None
    datetime: str
    status: str
    source: str
    latitude: float | None
    longitude: float | None
    address: str | None
    comment: str | None
    user: NotRequired[EmployeeShort]
    location: NotRequired[AttendanceListRowLocation]
    attachments: NotRequired[list[AttendanceListRowAttachment]]

class AttendanceListRowLocation(TypedDict):
    id: int
    external_id: str | None
    code: str | None
    title: str
    description: str | None
    latitude: float | None
    longitude: float | None
    radius: int
    created_at: str
    updated_at: str

class AttendanceListRowAttachment(TypedDict):
    id: int
    name: str
    description: str | None
    format: str
    url: str
    created_at: str

class AttendanceRecordResponse(TypedDict):
    data: list[AttendanceRecordRow]

class AttendanceRecordRow(TypedDict):
    user_id: int
    datetime: str
    status: str
    id: int
    result: str

class AttendanceRecordBody(TypedDict):
    # The marks to record, up to 100 a call.
    attendance: list[AttendanceRecordAttendanceItem]

class AttendanceRecordAttendanceItem(TypedDict):
    # The employee this belongs to, by the id this API issued.
    user_id: int
    # Where the mark was made, by id.
    location_id: NotRequired[int | None]
    # The shift this mark belongs to, by id, where you know which one it is.
    shift_id: NotRequired[int | None]
    # What the mark is: coming in, going out, or going on a break.
    status: AttendanceStatus
    # When it happened, as `2026-08-01T09:00:00+05:00`. The offset is part of it rather than
    # optional. Not in the future, and at most 24 hours late.
    datetime: str
    # A note carried alongside, for people to read.
    comment: NotRequired[str | None]

class DepartmentsListResponse(TypedDict):
    data: list[DepartmentsListRow]
    links: PageLinks
    meta: PageMeta

class DepartmentsListRow(TypedDict):
    id: int
    external_id: str | None
    title: str
    description: str | None
    created_at: str
    updated_at: str
    managers: NotRequired[list[EmployeeShort]]

class DepartmentsUpsertResponse(TypedDict):
    data: list[UpsertOutcome]

class DepartmentsUpsertBody(TypedDict):
    # The rows to write. Each carries your own `external_id`, and a row already stored under that
    # key is updated rather than added.
    items: list[DepartmentsUpsertItem]

class DepartmentsUpsertItem(TypedDict):
    # Your own key for this row. Send it on every write and the next one updates rather than
    # duplicates.
    external_id: str
    # The name this is shown under.
    title: str
    # Free text about this row, for people rather than for your code.
    description: NotRequired[str | None]

class DepartmentsGetResponse(TypedDict):
    data: DepartmentsGetData

class DepartmentsGetData(TypedDict):
    id: int
    external_id: str | None
    title: str
    description: str | None
    created_at: str
    updated_at: str
    managers: NotRequired[list[EmployeeShort]]

class DepartmentsDeleteResponse(TypedDict):
    data: DeleteOutcome

class DocumentsListResponse(TypedDict):
    data: list[DocumentsListRow]
    links: PageLinks
    meta: PageMeta

class DocumentsListRow(TypedDict):
    id: int
    external_id: str | None
    user_id: int
    author_id: int
    party: str
    type: str
    name: str
    contract_number: str | None
    employment_type: str | None
    start_date: str | None
    end_date: str | None
    expiration_date: str | None
    parent_document_id: int | None
    signature: DocumentsListRowSignature
    created_at: str
    updated_at: str
    attachments: NotRequired[list[DocumentsListRowAttachment]]
    signers: NotRequired[list[DocumentsListRowSigner]]
    labor_contract: NotRequired[DocumentsListRowLaborContract | None]

class DocumentsListRowSignature(TypedDict):
    state: str
    completed_at: str | None

class DocumentsListRowAttachment(TypedDict):
    id: int
    name: str
    description: str | None
    format: str
    url: str
    created_at: str

class DocumentsListRowSigner(TypedDict):
    type: str
    status: str
    signed_at: str | None
    signed_via: str | None
    party_id: int
    party_type: str

class DocumentsListRowLaborContract(TypedDict):
    id: int
    external_contract_id: str
    iin: str
    contract_number: str | None
    contract_date: str | None
    begin_date: str | None
    end_date: str | None
    termination_date: str | None
    established_post: str
    has_contract_file: bool

class DocumentsUpsertResponse(TypedDict):
    data: list[UpsertOutcome]

class DocumentsUpsertBody(TypedDict):
    # The documents to write, up to 100 a call.
    documents: list[DocumentsUpsertDocument]

class DocumentsUpsertDocument(TypedDict):
    # Your own key for this row. Send it on every write and the next one updates rather than
    # duplicates.
    external_id: str
    # Which kind of document this is.
    type: DocumentsType
    # The employee this belongs to, by the id this API issued.
    user_id: int
    # What to call this document.
    name: NotRequired[str | None]
    # The number written on the contract.
    contract_number: NotRequired[str | None]
    # The terms the contract is on.
    employment_type: NotRequired[DocumentsEmploymentType | None]
    # The day it begins, `YYYY-MM-DD`.
    start_date: NotRequired[str | None]
    # The day it ends, `YYYY-MM-DD`.
    end_date: NotRequired[str | None]
    # The day it stops being valid, `YYYY-MM-DD`.
    expiration_date: NotRequired[str | None]
    # The document this one hangs under, by your key for that one.
    parent_external_id: NotRequired[str | None]
    # The stored file this points at, from `POST /files`. Upload the bytes first and name the id it
    # answered with.
    file_id: NotRequired[int | None]

class DocumentsGetResponse(TypedDict):
    data: DocumentsGetData

class DocumentsGetData(TypedDict):
    id: int
    external_id: str | None
    user_id: int
    author_id: int
    party: str
    type: str
    name: str
    contract_number: str | None
    employment_type: str | None
    start_date: str | None
    end_date: str | None
    expiration_date: str | None
    parent_document_id: int | None
    signature: DocumentsGetDataSignature
    created_at: str
    updated_at: str
    attachments: NotRequired[list[DocumentsGetDataAttachment]]
    signers: NotRequired[list[DocumentsGetDataSigner]]
    labor_contract: NotRequired[DocumentsGetDataLaborContract | None]

class DocumentsGetDataSignature(TypedDict):
    state: str
    completed_at: str | None

class DocumentsGetDataAttachment(TypedDict):
    id: int
    name: str
    description: str | None
    format: str
    url: str
    created_at: str

class DocumentsGetDataSigner(TypedDict):
    type: str
    status: str
    signed_at: str | None
    signed_via: str | None
    party_id: int
    party_type: str

class DocumentsGetDataLaborContract(TypedDict):
    id: int
    external_contract_id: str
    iin: str
    contract_number: str | None
    contract_date: str | None
    begin_date: str | None
    end_date: str | None
    termination_date: str | None
    established_post: str
    has_contract_file: bool

class DocumentsDeleteResponse(TypedDict):
    data: DeleteOutcome

class FilesUploadResponse(TypedDict):
    data: FilesUploadData

class FilesUploadData(TypedDict):
    id: int
    name: str
    format: str
    url: str
    created_at: str

class LocationsListResponse(TypedDict):
    data: list[LocationsListRow]
    links: PageLinks
    meta: PageMeta

class LocationsListRow(TypedDict):
    id: int
    external_id: str | None
    code: str | None
    title: str
    description: str | None
    latitude: float | None
    longitude: float | None
    radius: int
    created_at: str
    updated_at: str
    managers: NotRequired[list[EmployeeShort]]

class LocationsUpsertResponse(TypedDict):
    data: list[UpsertOutcome]

class LocationsUpsertBody(TypedDict):
    # The rows to write. Each carries your own `external_id`, and a row already stored under that
    # key is updated rather than added.
    items: list[LocationsUpsertItem]

class LocationsUpsertItem(TypedDict):
    # Your own key for this row. Send it on every write and the next one updates rather than
    # duplicates.
    external_id: str
    # The name this is shown under.
    title: str
    # Free text about this row, for people rather than for your code.
    description: NotRequired[str | None]
    # A short code people read, yours to choose. The listing beside this write can filter on it.
    code: NotRequired[str | None]
    # Where the location is. A mobile clock-in is checked against this and `radius`.
    latitude: NotRequired[float | None]
    # Where the location is. A mobile clock-in is checked against this and `radius`.
    longitude: NotRequired[float | None]
    # How far from those coordinates a mobile clock-in still counts, in metres. A location written
    # without one gets 100.
    radius: NotRequired[int]

class LocationsGetResponse(TypedDict):
    data: LocationsGetData

class LocationsGetData(TypedDict):
    id: int
    external_id: str | None
    code: str | None
    title: str
    description: str | None
    latitude: float | None
    longitude: float | None
    radius: int
    created_at: str
    updated_at: str
    managers: NotRequired[list[EmployeeShort]]

class LocationsDeleteResponse(TypedDict):
    data: DeleteOutcome

class MeResponse(TypedDict):
    data: MeData

class MeData(TypedDict):
    id: int
    title: str

class PayrollPayslipsListResponse(TypedDict):
    data: list[PayrollPayslipsListRow]
    meta: PayrollPayslipsListMeta

class PayrollPayslipsListRow(TypedDict):
    id: int
    user: PayrollPayslipsListRowUser
    author_id: int
    period: PayrollPayslipsListRowPeriod
    status: str
    currency: str | None
    take_home: float
    ctc: int
    salary: PayrollPayslipsListRowSalary
    additions: list[PayrollPayslipsListRowAddition]
    deductions: list[PayrollPayslipsListRowDeduction]
    allowances: list[PayrollPayslipsListRowAddition]
    loan_repaid: int
    updated_at: str

class PayrollPayslipsListRowUser(TypedDict):
    id: int
    external_id: str | None

PayrollPayslipsListRowPeriod = TypedDict("PayrollPayslipsListRowPeriod", {"from": "str", "to": "str", "month": "str"})

class PayrollPayslipsListRowSalary(TypedDict):
    basic_rate: float | None
    basic_type: str | None
    work_days: int | None
    worked_days: int | None

class PayrollPayslipsListRowAddition(TypedDict):
    title: str
    type: str
    value: int
    pre_tax: bool
    comment: str | None

class PayrollPayslipsListRowDeduction(TypedDict):
    title: str
    type: str
    value: float
    pre_tax: bool
    comment: str | None

class PayrollPayslipsListMeta(TypedDict):
    per_page: int
    next_cursor: str | None
    prev_cursor: str | None

class PositionsListResponse(TypedDict):
    data: list[PositionsListRow]
    links: PageLinks
    meta: PageMeta

class PositionsListRow(TypedDict):
    id: int
    external_id: str | None
    title: str
    description: str | None
    created_at: str
    updated_at: str

class PositionsUpsertResponse(TypedDict):
    data: list[UpsertOutcome]

class PositionsUpsertBody(TypedDict):
    # The rows to write. Each carries your own `external_id`, and a row already stored under that
    # key is updated rather than added.
    items: list[PositionsUpsertItem]

class PositionsUpsertItem(TypedDict):
    # Your own key for this row. Send it on every write and the next one updates rather than
    # duplicates.
    external_id: str
    # The name this is shown under.
    title: str
    # Free text about this row, for people rather than for your code.
    description: NotRequired[str | None]

class PositionsGetResponse(TypedDict):
    data: PositionsGetData

class PositionsGetData(TypedDict):
    id: int
    external_id: str | None
    title: str
    description: str | None
    created_at: str
    updated_at: str

class PositionsDeleteResponse(TypedDict):
    data: DeleteOutcome

class SchedulesCreateResponse(TypedDict):
    data: list[SchedulesCreateRow]

class SchedulesCreateRow(TypedDict):
    id: int
    type: str
    leave_type: str | None
    is_split: bool
    dates: list[str]
    timezone: str | None
    start: str | None
    end: str | None
    time_planned: int
    break_time: int
    grace_start: int
    grace_end: int
    location_id: int | None
    department_id: int | None
    position_id: int | None
    shifts: list[SchedulesCreateRowShift]
    users: list[SchedulesCreateRowUser]

class SchedulesCreateRowShift(TypedDict):
    id: int
    start: str
    end: str
    time_planned: int
    location_id: int | None
    department_id: int | None
    position_id: int | None

class SchedulesCreateRowUser(TypedDict):
    id: int
    external_id: str | None

class SchedulesCreateBody(TypedDict):
    # The days to write, up to 25 a call. Each is one of three shapes, and `type` says which.
    schedules: list[WorkSchedule | FreeSchedule | LeaveSchedule]

class SchedulesGetResponse(TypedDict):
    data: SchedulesGetData

class SchedulesGetData(TypedDict):
    id: int
    type: str
    leave_type: str | None
    is_split: bool
    dates: list[str]
    timezone: str
    start: str
    end: str
    time_planned: int
    break_time: int
    grace_start: int
    grace_end: int
    location_id: int | None
    department_id: int | None
    position_id: int | None
    shifts: list[SchedulesGetDataShift]
    users: list[SchedulesGetDataUser]

class SchedulesGetDataShift(TypedDict):
    id: int
    start: str
    end: str
    time_planned: int
    location_id: int | None
    department_id: int | None
    position_id: int | None

class SchedulesGetDataUser(TypedDict):
    id: int
    external_id: str | None

class SchedulesDeleteResponse(TypedDict):
    data: DeleteOutcome

class TasksListResponse(TypedDict):
    data: list[TasksListRow]
    meta: TasksListMeta

class TasksListRow(TypedDict):
    id: int
    external_id: str | None
    title: str
    description: str | None
    status: str
    active: bool
    priority: int
    user_id: int
    author_id: int
    category_id: int | None
    location_id: int | None
    department_id: int | None
    position_id: int | None
    due_date: str
    time_start: str
    time_end: str
    timezone: str
    kpi_plan: int
    kpi_fact: int
    time_worked: int
    started_at: str | None
    finished_at: str | None
    created_at: str
    updated_at: str
    items: NotRequired[list[TasksListRowItem]]
    managers: NotRequired[list[EmployeeShort]]
    user: NotRequired[EmployeeShort]
    author: NotRequired[EmployeeShort]

class TasksListRowItem(TypedDict):
    id: int
    title: str
    order: int
    is_completed: bool

class TasksListMeta(TypedDict):
    per_page: int
    next_cursor: str | None
    prev_cursor: str | None

class TasksUpsertResponse(TypedDict):
    data: list[UpsertOutcome]

class TasksUpsertBody(TypedDict):
    # The tasks to write, up to 100 a call.
    tasks: list[TasksUpsertTask]

class TasksUpsertTask(TypedDict):
    # Your own key for this row. Send it on every write and the next one updates rather than
    # duplicates.
    external_id: str
    # The name this is shown under.
    title: str
    # Free text about this row, for people rather than for your code.
    description: NotRequired[str | None]
    # The employee this belongs to, by the id this API issued.
    user_id: int
    # The category it belongs to, by id.
    category_id: NotRequired[int | None]
    # The location this is filed against, by id. Null clears it.
    location_id: NotRequired[int | None]
    # The department this is filed against, by id. Null clears it.
    department_id: NotRequired[int | None]
    # The position this is filed against, by id. Null clears it.
    position_id: NotRequired[int | None]
    # The day it is due, `YYYY-MM-DD`.
    due_date: NotRequired[str | None]
    # When in the day it starts, as a clock time `HH:MM:SS`.
    time_start: NotRequired[str | None]
    # When in the day it ends, as a clock time `HH:MM:SS`.
    time_end: NotRequired[str | None]
    # The UTC offset the clock times beside it are read in — `Z`, or `+05:00`. An offset rather than
    # a zone name, so the day is fixed to a moment rather than to a rule that may be changed later.
    timezone: NotRequired[str | None]
    # Whether the task is flagged as a priority: `1` if it is, `0` if not.
    priority: NotRequired[TasksPriority]
    # Whether the task is active.
    active: NotRequired[bool]
    # The planned figure this task is measured against.
    kpi_plan: NotRequired[float | None]
    # Who may decide on this task, by id. Up to ten.
    managers: NotRequired[list[int] | None]
    # The checklist inside this task, in the order given.
    items: NotRequired[list[TasksUpsertTaskItem] | None]

class TasksUpsertTaskItem(TypedDict):
    # The name this is shown under.
    title: str
    # Where this item sits in the checklist, counting from zero.
    order: NotRequired[int | None]

class TasksGetResponse(TypedDict):
    data: TasksGetData

class TasksGetData(TypedDict):
    id: int
    external_id: str | None
    title: str
    description: str | None
    status: str
    active: bool
    priority: int
    user_id: int
    author_id: int
    category_id: int | None
    location_id: int | None
    department_id: int | None
    position_id: int | None
    due_date: str
    time_start: str
    time_end: str
    timezone: str
    kpi_plan: int
    kpi_fact: int
    time_worked: int
    started_at: str | None
    finished_at: str | None
    created_at: str
    updated_at: str
    items: NotRequired[list[TasksGetDataItem]]
    managers: NotRequired[list[EmployeeShort]]
    user: NotRequired[EmployeeShort]
    author: NotRequired[EmployeeShort]

class TasksGetDataItem(TypedDict):
    id: int
    title: str
    order: int
    is_completed: bool

class TimesheetsListResponse(TypedDict):
    data: list[TimesheetsListRow]
    meta: TimesheetsListMeta

class TimesheetsListRow(TypedDict):
    date: str
    user: TimesheetsListRowUser
    planned: TimesheetsListRowPlanned | None
    actual: NotRequired[TimesheetsListRowActual]
    variance: NotRequired[TimesheetsListRowVariance]

class TimesheetsListRowUser(TypedDict):
    id: int
    external_id: str | None
    code: NotRequired[str | None]
    first_name: NotRequired[str]
    middle_name: NotRequired[str | None]
    last_name: NotRequired[str]

class TimesheetsListRowPlanned(TypedDict):
    schedule_id: int
    type: str
    leave_type: str | None
    is_split: bool
    timezone: str
    start: str
    end: str
    time_planned: int
    break_time: int
    grace_start: int
    grace_end: int
    shifts: list[TimesheetsListRowPlannedShift]
    location_id: int | None
    department_id: int | None
    position_id: int | None
    location: NotRequired[TimesheetsListRowPlannedShiftLocation | None]
    department: NotRequired[TimesheetsListRowPlannedShiftLocation | None]
    position: NotRequired[TimesheetsListRowPlannedShiftLocation | None]

class TimesheetsListRowPlannedShift(TypedDict):
    id: int
    code: str | None
    start: str
    end: str
    time_planned: int
    location_id: int | None
    department_id: int | None
    position_id: int | None
    location: NotRequired[TimesheetsListRowPlannedShiftLocation | None]
    department: NotRequired[TimesheetsListRowPlannedShiftLocation | None]
    position: NotRequired[TimesheetsListRowPlannedShiftLocation | None]

class TimesheetsListRowPlannedShiftLocation(TypedDict):
    id: int
    external_id: str | None
    title: str

TimesheetsListRowActual = TypedDict("TimesheetsListRowActual", {"in": "str | None", "out": "str | None", "time_worked": "int", "time_break": "int", "time_worked_day_off": "int", "time_night": "int", "shifts": "list[TimesheetsListRowActualShift]"})

TimesheetsListRowActualShift = TypedDict("TimesheetsListRowActualShift", {"id": "int", "in": "str", "out": "str", "time_worked": "int"})

class TimesheetsListRowVariance(TypedDict):
    time_late: int
    time_early_left: int
    time_overworked: int
    time_underworked: int

class TimesheetsListMeta(TypedDict):
    users_per_page: int
    next_cursor: str | None
    prev_cursor: str | None

class UserFiltersListResponse(TypedDict):
    data: list[UserFiltersListRow]
    links: PageLinks
    meta: PageMeta

class UserFiltersListRow(TypedDict):
    id: int
    external_id: str | None
    title: str
    description: str | None
    created_at: str
    updated_at: str
    managers: NotRequired[list[EmployeeShort]]

class UserFiltersUpsertResponse(TypedDict):
    data: list[UpsertOutcome]

class UserFiltersUpsertBody(TypedDict):
    # The rows to write. Each carries your own `external_id`, and a row already stored under that
    # key is updated rather than added.
    items: list[UserFiltersUpsertItem]

class UserFiltersUpsertItem(TypedDict):
    # Your own key for this row. Send it on every write and the next one updates rather than
    # duplicates.
    external_id: str
    # The name this is shown under.
    title: str
    # Free text about this row, for people rather than for your code.
    description: NotRequired[str | None]

class UserFiltersGetResponse(TypedDict):
    data: UserFiltersGetData

class UserFiltersGetData(TypedDict):
    id: int
    external_id: str | None
    title: str
    description: str | None
    created_at: str
    updated_at: str
    managers: NotRequired[list[EmployeeShort]]

class UserFiltersDeleteResponse(TypedDict):
    data: DeleteOutcome

class UserRequestsListResponse(TypedDict):
    data: list[UserRequestsListRow]
    links: PageLinks
    meta: PageMeta

class UserRequestsListRow(TypedDict):
    id: str
    type: str
    subtype: str | None
    status: str
    user_id: int
    author_id: int
    period: UserRequestsListRowPeriod
    comment: str | None
    amount: float | None
    currency: str | None
    created_at: str
    updated_at: str
    user: NotRequired[EmployeeShort]
    author: NotRequired[EmployeeShort]
    content: NotRequired[UserRequestsListRowContent]

class UserRequestsListRowPeriod(TypedDict):
    date_start: str | None
    date_end: str | None

class UserRequestsListRowContent(TypedDict):
    type: str
    clockins: NotRequired[list[UserRequestsListRowContentClockin]]
    amount: NotRequired[float | None]
    currency_id: NotRequired[int]

class UserRequestsListRowContentClockin(TypedDict):
    status: str
    datetime: str

class UserRequestsGetResponse(TypedDict):
    data: UserRequestsGetData

class UserRequestsGetData(TypedDict):
    id: str
    type: str
    subtype: str | None
    status: str
    user_id: int
    author_id: int
    period: UserRequestsGetDataPeriod
    comment: str | None
    amount: float | None
    currency: str | None
    created_at: str
    updated_at: str
    content: UserRequestsGetDataContent

class UserRequestsGetDataPeriod(TypedDict):
    date_start: str
    date_end: str

class UserRequestsGetDataContent(TypedDict):
    type: str
    clockins: list[UserRequestsGetDataContentClockin]

class UserRequestsGetDataContentClockin(TypedDict):
    status: str
    datetime: str

class UsersListResponse(TypedDict):
    data: list[UsersListRow]
    links: PageLinks
    meta: PageMeta

class UsersListRow(TypedDict):
    id: int
    external_id: str | None
    code: str | None
    first_name: str
    middle_name: str | None
    last_name: str
    email: str
    phone: str | None
    extra_phone: str | None
    role: str | None
    gender: str
    national_id: str
    tax_id: str | None
    insurance_id: str | None
    employment: str
    locale: str
    timezone: str
    date_birth: str
    date_hire: str
    date_leave: str | None
    photo: str | None
    created_at: str
    updated_at: str
    dismissed_at: str | None
    dismissal: NotRequired[UsersListRowDismissal]
    location: NotRequired[UsersListRowLocation]
    locations: NotRequired[list[UsersListRowLocation]]
    department: NotRequired[UsersListRowDepartment]
    position: NotRequired[UsersListRowDepartment]
    user_filters: NotRequired[list[UsersListRowDepartment]]
    meta: NotRequired[UsersListRowMeta]

class UsersListRowDismissal(TypedDict):
    id: int
    title: str

class UsersListRowLocation(TypedDict):
    id: int
    external_id: str | None
    code: str | None
    title: str
    description: str | None
    latitude: float | None
    longitude: float | None
    radius: int
    created_at: str
    updated_at: str

class UsersListRowDepartment(TypedDict):
    id: int
    external_id: str | None
    title: str
    description: str | None
    created_at: str
    updated_at: str

class UsersListRowMeta(TypedDict):
    birth_place: str
    marital_status: str
    religion: str | None
    blood_type: str | None
    children: int | None
    contact_name: str | None
    relationship: str | None
    phone: str | None
    domicile_address: str | None
    domicile_city: str | None
    domicile_province: str | None
    domicile_district: str | None
    domicile_postal_code: str | None
    document_address: str | None
    document_city: str | None
    document_province: str | None
    document_district: str | None
    document_postal_code: str | None
    education_level: str | None
    education_institution: str | None
    education_major: str | None
    graduation_year: int | None
    education_gpa: float | None
    full_name: str | None
    alias_name: str | None
    local_name: str | None
    nationality: str | None
    marriage_date: str | None
    retire_age: int | None
    retire_date: str | None
    ethnic_origin: str | None
    contract_number: str | None
    health_insurance_id: str | None
    gov_savings_id: str | None
    gov_savings_acc: str | None

class UsersDismissResponse(TypedDict):
    data: list[UpsertOutcome]

class UsersDismissBody(TypedDict):
    # The people to dismiss, up to 100 a call.
    users: list[UsersDismissUser]

class UsersDismissUser(TypedDict):
    # Who to dismiss, by your key for them. This or `id`, exactly one per item.
    external_id: NotRequired[str]
    # Who to dismiss, by the id this API issued. This or `external_id`, exactly one per item.
    id: NotRequired[int]

class UsersUpsertResponse(TypedDict):
    data: list[UpsertOutcome]

class UsersUpsertBody(TypedDict):
    # The people to write, up to 100 a call.
    users: list[UsersUpsertUser]

class UsersUpsertUser(TypedDict):
    # Your own key for this row. Send it on every write and the next one updates rather than
    # duplicates.
    external_id: NotRequired[str | None]
    # Given name. The one field every person must have.
    first_name: str
    # Middle name, where the place they live uses one.
    middle_name: NotRequired[str | None]
    # Family name.
    last_name: NotRequired[str | None]
    # A short code people read, yours to choose. The listing beside this write can filter on it.
    code: NotRequired[str | None]
    # Their email address.
    email: NotRequired[str | None]
    # Their phone number.
    phone: NotRequired[str | None]
    # A second phone number.
    extra_phone: NotRequired[str | None]
    # Whether the person administers the company or is an employee in it.
    role: UsersRole
    # Their gender, as the personnel file records it.
    gender: NotRequired[UsersGender | None]
    # Which language the application speaks to them in.
    locale: NotRequired[UsersLocale | None]
    # The zone they work in, as a name — `Asia/Almaty`. A name rather than an offset, unlike a
    # schedule or a task, because a person's zone follows the rules of the place they are in.
    timezone: NotRequired[str | None]
    # The day they started, `YYYY-MM-DD`.
    date_hire: NotRequired[str | None]
    # The day they leave or left, `YYYY-MM-DD`. Filled in for you on a dismissal that does not carry
    # one.
    date_leave: NotRequired[str | None]
    # Their date of birth, `YYYY-MM-DD`.
    date_birth: NotRequired[str | None]
    # Their national identifier.
    national_id: NotRequired[str | None]
    # Their tax identifier.
    tax_id: NotRequired[str | None]
    # Their insurance identifier.
    insurance_id: NotRequired[str | None]
    # The terms they are employed on.
    employment: NotRequired[UsersEmployment | None]
    # Free text about what this person is responsible for.
    responsibility: NotRequired[str | None]
    # The location they are filed under, by id. Required — everybody belongs somewhere.
    location_id: int
    # Every other location they may work at, by id, beside the one they are filed under.
    locations: NotRequired[list[int] | None]
    # The department this is filed against, by id. Null clears it.
    department_id: NotRequired[int | None]
    # The position this is filed against, by id. Null clears it.
    position_id: NotRequired[int | None]
    # The groupings they belong to, by id.
    user_filters: NotRequired[list[int] | None]

class UsersGetResponse(TypedDict):
    data: UsersGetData

class UsersGetData(TypedDict):
    id: int
    external_id: str | None
    code: str | None
    first_name: str
    middle_name: str | None
    last_name: str
    email: str
    phone: str | None
    extra_phone: str | None
    role: str | None
    gender: str
    national_id: str
    tax_id: str | None
    insurance_id: str | None
    employment: str
    locale: str
    timezone: str
    date_birth: str
    date_hire: str
    date_leave: str | None
    photo: str | None
    created_at: str
    updated_at: str
    dismissed_at: str | None
    location: NotRequired[UsersGetDataLocation]
    locations: NotRequired[list[UsersGetDataLocation]]
    department: NotRequired[UsersGetDataDepartment]
    position: NotRequired[UsersGetDataDepartment]
    user_filters: NotRequired[list[UsersGetDataDepartment]]
    dismissal: NotRequired[UsersGetDataDismissal]
    meta: NotRequired[UsersGetDataMeta]

class UsersGetDataLocation(TypedDict):
    id: int
    external_id: str | None
    code: str | None
    title: str
    description: str | None
    latitude: float | None
    longitude: float | None
    radius: int
    created_at: str
    updated_at: str

class UsersGetDataDepartment(TypedDict):
    id: int
    external_id: str | None
    title: str
    description: str | None
    created_at: str
    updated_at: str

class UsersGetDataDismissal(TypedDict):
    id: int
    title: str

class UsersGetDataMeta(TypedDict):
    birth_place: str
    marital_status: str
    religion: str | None
    blood_type: str | None
    children: int | None
    contact_name: str | None
    relationship: str | None
    phone: str | None
    domicile_address: str | None
    domicile_city: str | None
    domicile_province: str | None
    domicile_district: str | None
    domicile_postal_code: str | None
    document_address: str | None
    document_city: str | None
    document_province: str | None
    document_district: str | None
    document_postal_code: str | None
    education_level: str | None
    education_institution: str | None
    education_major: str | None
    graduation_year: int | None
    education_gpa: float | None
    full_name: str | None
    alias_name: str | None
    local_name: str | None
    nationality: str | None
    marriage_date: str | None
    retire_age: int | None
    retire_date: str | None
    ethnic_origin: str | None
    contract_number: str | None
    health_insurance_id: str | None
    gov_savings_id: str | None
    gov_savings_acc: str | None

class WebhooksListResponse(TypedDict):
    data: list[WebhooksListRow]
    links: PageLinks
    meta: PageMeta

class WebhooksListRow(TypedDict):
    id: int
    title: str
    url: str
    contact_email: str
    secret: str
    events: list[str]
    auth: WebhooksListRowAuth
    active: bool
    health: WebhooksListRowHealth

class WebhooksListRowAuth(TypedDict):
    type: str
    username: str | None

class WebhooksListRowHealth(TypedDict):
    consecutive_failures: int
    last_success_at: str | None
    last_failure_at: str | None
    last_failure_status: int | None
    disabled_at: str | None
    disabled_reason: str | None

class WebhooksCreateResponse(TypedDict):
    data: WebhooksCreateData

class WebhooksCreateData(TypedDict):
    id: int
    title: str
    url: str
    contact_email: str
    secret: str
    events: list[str]
    auth: WebhooksCreateDataAuth
    active: bool
    health: WebhooksCreateDataHealth

class WebhooksCreateDataAuth(TypedDict):
    type: str
    username: str | None

class WebhooksCreateDataHealth(TypedDict):
    consecutive_failures: int
    last_success_at: str | None
    last_failure_at: str | None
    last_failure_status: int | None
    disabled_at: str | None
    disabled_reason: str | None

class WebhooksCreateBody(TypedDict):
    # What to call this endpoint, so a list of them reads.
    title: NotRequired[str | None]
    # Where deliveries are posted. `http` or `https`.
    url: str
    # An address to reach you about this endpoint.
    contact_email: NotRequired[str | None]
    # Which events this endpoint receives. At least one, and no repeats.
    events: list[WebhooksEvent]
    # Send deliveries with HTTP basic authentication. Not alongside `auth_token`.
    auth_basic: NotRequired[WebhooksCreateAuthBasic | None]
    # Send deliveries carrying this bearer token. Not alongside `auth_basic`.
    auth_token: NotRequired[str | None]
    # Whether the endpoint receives deliveries. False stops them without deleting it.
    active: bool

class WebhooksCreateAuthBasic(TypedDict):
    # The user for `auth_basic`.
    username: NotRequired[str]
    # The password for `auth_basic`.
    password: NotRequired[str]

class WebhooksDeliveriesListResponse(TypedDict):
    data: list[WebhooksDeliveriesListRow]
    links: PageLinks
    meta: PageMeta

class WebhooksDeliveriesListRow(TypedDict):
    id: int
    webhook_id: int
    event: str
    state: str
    attempts: int
    response_status: int
    failure_reason: str | None
    occurred_at: str
    next_attempt_at: str | None
    processed_at: str | None
    payload: NotRequired[WebhooksDeliveriesListRowPayload]

class WebhooksDeliveriesListRowPayload(TypedDict):
    id: int

class WebhooksDeliveriesGetResponse(TypedDict):
    data: WebhooksDeliveriesGetData

class WebhooksDeliveriesGetData(TypedDict):
    id: int
    webhook_id: int
    event: str
    state: str
    attempts: int
    response_status: int
    failure_reason: str | None
    occurred_at: str
    next_attempt_at: str | None
    processed_at: str
    payload: WebhooksDeliveriesGetDataPayload

class WebhooksDeliveriesGetDataPayload(TypedDict):
    id: int

class WebhooksDeliveriesRedeliverResponse(TypedDict):
    data: DeleteOutcome

class WebhooksEventsListResponse(TypedDict):
    data: list[str]

class WebhooksGetResponse(TypedDict):
    data: WebhooksGetData

class WebhooksGetData(TypedDict):
    id: int
    title: str
    url: str
    contact_email: str
    secret: str
    events: list[str]
    auth: WebhooksGetDataAuth
    active: bool
    health: WebhooksGetDataHealth

class WebhooksGetDataAuth(TypedDict):
    type: str
    username: str | None

class WebhooksGetDataHealth(TypedDict):
    consecutive_failures: int
    last_success_at: str | None
    last_failure_at: str | None
    last_failure_status: int | None
    disabled_at: str | None
    disabled_reason: str | None

class WebhooksUpdateResponse(TypedDict):
    data: WebhooksUpdateData

class WebhooksUpdateData(TypedDict):
    id: int
    title: str
    url: str
    contact_email: str
    secret: str
    events: list[str]
    auth: WebhooksUpdateDataAuth
    active: bool
    health: WebhooksUpdateDataHealth

class WebhooksUpdateDataAuth(TypedDict):
    type: str
    username: str | None

class WebhooksUpdateDataHealth(TypedDict):
    consecutive_failures: int
    last_success_at: str | None
    last_failure_at: str | None
    last_failure_status: int | None
    disabled_at: str | None
    disabled_reason: str | None

class WebhooksUpdateBody(TypedDict):
    # What to call this endpoint, so a list of them reads.
    title: NotRequired[str | None]
    # Where deliveries are posted. `http` or `https`.
    url: str
    # An address to reach you about this endpoint.
    contact_email: NotRequired[str | None]
    # Which events this endpoint receives. At least one, and no repeats.
    events: list[WebhooksEvent]
    # Send deliveries with HTTP basic authentication. Not alongside `auth_token`.
    auth_basic: NotRequired[WebhooksUpdateAuthBasic | None]
    # Send deliveries carrying this bearer token. Not alongside `auth_basic`.
    auth_token: NotRequired[str | None]
    # Whether the endpoint receives deliveries. False stops them without deleting it.
    active: bool

class WebhooksUpdateAuthBasic(TypedDict):
    # The user for `auth_basic`.
    username: NotRequired[str]
    # The password for `auth_basic`.
    password: NotRequired[str]

class WebhooksDeleteResponse(TypedDict):
    data: DeleteOutcome

class WebhooksRotateSecretResponse(TypedDict):
    data: WebhooksRotateSecretData

class WebhooksRotateSecretData(TypedDict):
    id: int
    title: str
    url: str
    contact_email: str
    secret: str
    events: list[str]
    auth: WebhooksRotateSecretDataAuth
    active: bool
    health: WebhooksRotateSecretDataHealth

class WebhooksRotateSecretDataAuth(TypedDict):
    type: str
    username: str | None

class WebhooksRotateSecretDataHealth(TypedDict):
    consecutive_failures: int
    last_success_at: str | None
    last_failure_at: str | None
    last_failure_status: int | None
    disabled_at: str | None
    disabled_reason: str | None
