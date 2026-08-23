# Changelog

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
