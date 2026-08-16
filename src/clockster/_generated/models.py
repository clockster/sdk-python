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
    "AttendanceListResponse",
    "AttendanceListRow",
    "AttendanceListRowAttachment",
    "AttendanceListRowLocation",
    "AttendanceRecordAttendanceItem",
    "AttendanceRecordBody",
    "AttendanceRecordResponse",
    "AttendanceRecordRow",
    "DeleteOutcome",
    "DepartmentsDeleteResponse",
    "DepartmentsGetData",
    "DepartmentsGetResponse",
    "DepartmentsListResponse",
    "DepartmentsListRow",
    "DepartmentsUpsertBody",
    "DepartmentsUpsertItem",
    "DepartmentsUpsertResponse",
    "DocumentsDeleteResponse",
    "DocumentsGetData",
    "DocumentsGetDataAttachment",
    "DocumentsGetDataLaborContract",
    "DocumentsGetDataSignature",
    "DocumentsGetDataSigner",
    "DocumentsGetResponse",
    "DocumentsListResponse",
    "DocumentsListRow",
    "DocumentsListRowAttachment",
    "DocumentsListRowLaborContract",
    "DocumentsListRowSignature",
    "DocumentsListRowSigner",
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
    "TasksGetData",
    "TasksGetDataItem",
    "TasksGetResponse",
    "TasksListMeta",
    "TasksListResponse",
    "TasksListRow",
    "TasksListRowItem",
    "TasksUpsertBody",
    "TasksUpsertResponse",
    "TasksUpsertTask",
    "TasksUpsertTaskItem",
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
    "UserRequestsListResponse",
    "UserRequestsListRow",
    "UserRequestsListRowContent",
    "UserRequestsListRowContentClockin",
    "UserRequestsListRowPeriod",
    "UsersDismissBody",
    "UsersDismissResponse",
    "UsersDismissUser",
    "UsersGetData",
    "UsersGetDataDepartment",
    "UsersGetDataDismissal",
    "UsersGetDataLocation",
    "UsersGetDataMeta",
    "UsersGetResponse",
    "UsersListResponse",
    "UsersListRow",
    "UsersListRowDepartment",
    "UsersListRowDismissal",
    "UsersListRowLocation",
    "UsersListRowMeta",
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
    "WebhooksDeliveriesListResponse",
    "WebhooksDeliveriesListRow",
    "WebhooksDeliveriesListRowPayload",
    "WebhooksDeliveriesRedeliverResponse",
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


class WorkSchedule(TypedDict):
    type: Literal["work", "free", "leave"]
    dates: list[str]
    users: list[int]
    location_id: NotRequired[int | None]
    department_id: NotRequired[int | None]
    position_id: NotRequired[int | None]
    timezone: str
    start: NotRequired[str | None]
    end: NotRequired[str | None]
    break_time: NotRequired[int | None]
    grace_start: NotRequired[int | None]
    grace_end: NotRequired[int | None]
    shifts: NotRequired[list[WorkScheduleShift] | None]

class WorkScheduleShift(TypedDict):
    start: str
    end: str
    location_id: NotRequired[int | None]
    department_id: NotRequired[int | None]
    position_id: NotRequired[int | None]

class FreeSchedule(TypedDict):
    type: Literal["work", "free", "leave"]
    dates: list[str]
    users: list[int]
    location_id: NotRequired[int | None]
    department_id: NotRequired[int | None]
    position_id: NotRequired[int | None]
    timezone: str
    start: str
    end: str
    time_planned: NotRequired[int | None]

class LeaveSchedule(TypedDict):
    type: Literal["work", "free", "leave"]
    dates: list[str]
    users: list[int]
    location_id: NotRequired[int | None]
    department_id: NotRequired[int | None]
    position_id: NotRequired[int | None]
    leave_type: Literal["annual", "unpaid", "sick", "unpaid_sick", "maternity", "paternity", "special", "day_off", "compensatory", "personal", "emergency", "unexcused_absence"]

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
    attendance: list[AttendanceRecordAttendanceItem]

class AttendanceRecordAttendanceItem(TypedDict):
    user_id: int
    location_id: NotRequired[int | None]
    shift_id: NotRequired[int | None]
    status: Literal["out", "in", "break"]
    datetime: str
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
    items: list[DepartmentsUpsertItem]

class DepartmentsUpsertItem(TypedDict):
    external_id: str
    title: str
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
    documents: list[DocumentsUpsertDocument]

class DocumentsUpsertDocument(TypedDict):
    external_id: str
    type: Literal["passport", "cv", "diploma", "medical", "photo", "other", "medical_book", "employment_agreement", "termination_of_employment_agreement", "equipment_agreement", "application", "order", "supplementary_agreement", "job_description", "nda", "non_compete_agreement", "data_processing_agreement", "act_of_service_acceptance", "health_and_safety_briefing", "shift_schedule", "letter", "vacation_schedule", "contract", "agreement", "goods_release_note", "reconciliation_act", "return_to_supplier"]
    user_id: int
    name: NotRequired[str | None]
    contract_number: NotRequired[str | None]
    employment_type: NotRequired[Literal["full_time", "part_time", "irregular_hours", "contract_1", "contract_2", "apprenticeship", "traineeship", "piece_rate", "probation", "outstaffing"] | None]
    start_date: NotRequired[str | None]
    end_date: NotRequired[str | None]
    expiration_date: NotRequired[str | None]
    parent_external_id: NotRequired[str | None]
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
    items: list[LocationsUpsertItem]

class LocationsUpsertItem(TypedDict):
    external_id: str
    title: str
    description: NotRequired[str | None]
    code: NotRequired[str | None]
    latitude: NotRequired[float | None]
    longitude: NotRequired[float | None]
    radius: NotRequired[int | None]

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
    items: list[PositionsUpsertItem]

class PositionsUpsertItem(TypedDict):
    external_id: str
    title: str
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
    tasks: list[TasksUpsertTask]

class TasksUpsertTask(TypedDict):
    external_id: str
    title: str
    description: NotRequired[str | None]
    user_id: int
    category_id: NotRequired[int | None]
    location_id: NotRequired[int | None]
    department_id: NotRequired[int | None]
    position_id: NotRequired[int | None]
    due_date: NotRequired[str | None]
    time_start: NotRequired[str | None]
    time_end: NotRequired[str | None]
    timezone: NotRequired[str | None]
    priority: NotRequired[int]
    active: NotRequired[bool]
    kpi_plan: NotRequired[float | None]
    managers: NotRequired[list[int] | None]
    items: NotRequired[list[TasksUpsertTaskItem] | None]

class TasksUpsertTaskItem(TypedDict):
    title: str
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
    items: list[UserFiltersUpsertItem]

class UserFiltersUpsertItem(TypedDict):
    external_id: str
    title: str
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
    users: list[UsersDismissUser]

class UsersDismissUser(TypedDict):
    external_id: NotRequired[str]
    id: NotRequired[int]

class UsersUpsertResponse(TypedDict):
    data: list[UpsertOutcome]

class UsersUpsertBody(TypedDict):
    users: list[UsersUpsertUser]

class UsersUpsertUser(TypedDict):
    external_id: NotRequired[str | None]
    first_name: str
    middle_name: NotRequired[str | None]
    last_name: NotRequired[str | None]
    code: NotRequired[str | None]
    email: NotRequired[str | None]
    phone: NotRequired[str | None]
    extra_phone: NotRequired[str | None]
    role: Literal["admin", "employee"]
    gender: NotRequired[Literal["male", "female", "other"] | None]
    locale: NotRequired[Literal["en", "ru", "kk", "uk", "id", "uz", "az", "fr", "vi", "zh"] | None]
    timezone: NotRequired[str | None]
    date_hire: NotRequired[str | None]
    date_leave: NotRequired[str | None]
    date_birth: NotRequired[str | None]
    national_id: NotRequired[str | None]
    tax_id: NotRequired[str | None]
    insurance_id: NotRequired[str | None]
    employment: NotRequired[Literal["full_time", "part_time", "irregular_hours", "contract_1", "contract_2", "apprenticeship", "traineeship", "piece_rate", "probation", "outstaffing"] | None]
    responsibility: NotRequired[str | None]
    location_id: int
    locations: NotRequired[list[int] | None]
    department_id: NotRequired[int | None]
    position_id: NotRequired[int | None]
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
    title: NotRequired[str | None]
    url: str
    contact_email: NotRequired[str | None]
    events: list[Literal["user.created", "user.updated", "user.deleted", "user.restored", "user.purged", "location.created", "location.updated", "location.deleted", "department.created", "department.updated", "department.deleted", "position.created", "position.updated", "position.deleted", "task.created", "task.completed", "task.approved", "task.rejected", "task.deleted"]]
    auth_basic: NotRequired[WebhooksCreateAuthBasic | None]
    auth_token: NotRequired[str | None]
    active: bool

class WebhooksCreateAuthBasic(TypedDict):
    username: NotRequired[str]
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
    title: NotRequired[str | None]
    url: str
    contact_email: NotRequired[str | None]
    events: list[Literal["user.created", "user.updated", "user.deleted", "user.restored", "user.purged", "location.created", "location.updated", "location.deleted", "department.created", "department.updated", "department.deleted", "position.created", "position.updated", "position.deleted", "task.created", "task.completed", "task.approved", "task.rejected", "task.deleted"]]
    auth_basic: NotRequired[WebhooksUpdateAuthBasic | None]
    auth_token: NotRequired[str | None]
    active: bool

class WebhooksUpdateAuthBasic(TypedDict):
    username: NotRequired[str]
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
