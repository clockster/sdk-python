# Changelog

## 0.4.0

### May break your build (types only)

Nothing. Three operations and one set are new.

### Changed in the API

Reaches you whether or not you update this package.

- `GET /payroll/payslips` answers the `external_id` of a dismissed employee. It was `None` on their
  payslips.

### New

- `clockster.payroll.single_adjustments`: `list`, `create` and `delete`, blocking and awaited, over
  `/payroll/single-adjustments` — one-off additions and deductions that the next calculation of a
  payslip takes in. `create` files up to 100 at a time, all or nothing; pass `idempotency_key=` so a
  retry does not file them twice.
- `PayrollSingleAdjustmentsType` in `clockster.models`, a `Literal` of the six types, for `type` on
  `create` and the `types` filter.

## 0.3.0

### May break your build (types only)

Nothing. The five values are additive.

### Changed in the API

Reaches you whether or not you update this package.

- A document's `type` also takes `driver_license`, `birth_certificate`, `marriage_certificate`,
  `divorce_certificate` and `change_fio_certificate` — in the `types` filter and in
  `POST /documents/upsert`.

## 0.2.0

### May break your build (types only)

Nothing changes on the wire. Defer with `# type: ignore` if you need to.

- `radius` no longer accepts `None`.
- `priority` is now `Literal[0, 1]` rather than `int`.

### Changed in the API

Reaches you whether or not you update this package.

- A location's `radius` must be between 50 and 700. A value outside that is refused.
- `radius` cannot be cleared. Leave the key out to keep what is stored.
- `?employment=` takes only the ten terms of the set. An unknown one is refused rather than
  answering an empty page.

### New

- Every set of values is a named `Literal` in `clockster.models` — `UsersRole` rather than the
  values spelled out at each use. `typing.get_args()` answers with them.
- Every request body field carries its description as a comment above it.
