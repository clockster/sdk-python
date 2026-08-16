"""Generate src/clockster/_generated from openapi/company-v3.json.

The output is committed, so an API change appears in review as the lines of the client it moves.

Two files come out of it. `models.py` holds a TypedDict per shape the document describes: the
components it names, and one per request body and answer besides. `api.py` holds the namespaces —
`clockster.users.list(...)` — twice over, once blocking and once not.

Nothing here validates at run time. A response is the JSON as it arrived, and the types are
annotations a checker reads and the interpreter throws away; a field the API adds tomorrow reaches
the caller today rather than raising on the way in.
"""

from __future__ import annotations

import json
import keyword
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

SPEC = ROOT / "openapi" / "company-v3.json"

OUT = ROOT / "src" / "clockster" / "_generated"

PREFIX = "company.v3."

# Resource-controller verbs of the operation ids, mapped to the vocabulary of the SDK. The same
# table the TypeScript client uses, so one operation is called one thing in both.
VERBS = {"index": "list", "show": "get", "store": "create", "destroy": "delete"}

# Operations whose summary names a verb the map cannot reach, and two listings without an `index`.
OVERRIDES = {
    "company.v3.attendance.store": ("attendance", "record"),
    "company.v3.files.store": ("files", "upload"),
    "company.v3.webhooks.secret": ("webhooks", "rotate_secret"),
    "company.v3.payroll.payslips": ("payroll", "payslips", "list"),
    "company.v3.webhooks.events": ("webhooks", "events", "list"),
}

SCALARS = {"string": "str", "integer": "int", "number": "float", "boolean": "bool", "null": "None"}


def snake(name: str) -> str:
    """A Python name for a segment of an operation id."""
    out = re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_").lower()

    return f"{out}_" if keyword.iskeyword(out) else out


def camel(name: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[^a-zA-Z0-9]+", name) if part)


def singular(name: str) -> str:
    """`Shifts` is a list of `Shift`, and `Attendance` is a list of `Attendance`."""
    # The rows of a listing are what a caller iterates, and `UsersListRow` is what to call one.
    if name.endswith("Data"):
        return f"{name[:-4]}Row"

    if name.endswith("ies"):
        return f"{name[:-3]}y"

    if name.endswith("ss") or not name.endswith("s"):
        return f"{name}Item"

    return name[:-1]


class Models:
    """Every TypedDict the document implies, named once and in the order they were needed."""

    def __init__(self, document: dict[str, Any]) -> None:
        self.document = document
        self.blocks: dict[str, str] = {}
        # One operation's shapes, so the same object under two keys of one answer is named once.
        self.scope = ""
        self.shapes: dict[tuple[str, str], str] = {}

    def component(self, ref: str) -> str:
        name = ref.rsplit("/", 1)[-1]

        if name not in self.blocks:
            # Reserved before the body is built: a component that reaches itself would otherwise
            # recur forever.
            self.blocks[name] = ""
            self.blocks[name] = self.typed_dict(name, self.document["components"]["schemas"][name])

        return name

    def type_of(self, schema: dict[str, Any], hint: str) -> str:
        if "$ref" in schema:
            return self.component(schema["$ref"])

        if "oneOf" in schema:
            return " | ".join(self.type_of(one, hint) for one in schema["oneOf"])

        declared = schema.get("type")
        types = declared if isinstance(declared, list) else [declared]
        nullable = "null" in types
        rest = [one for one in types if one != "null" and one is not None]

        if not rest:
            return "None" if nullable else "Any"

        body = " | ".join(self.one_type(schema, one, hint) for one in rest)

        return f"{body} | None" if nullable else body

    def one_type(self, schema: dict[str, Any], declared: str, hint: str) -> str:
        if declared == "array":
            items = schema.get("items")

            return f"list[{self.type_of(items, singular(hint))}]" if items else "list[Any]"

        if declared == "object":
            return self.object_type(schema, hint)

        if declared == "string" and schema.get("enum"):
            return "Literal[" + ", ".join(json.dumps(value) for value in schema["enum"]) + "]"

        return SCALARS[declared]

    def object_type(self, schema: dict[str, Any], hint: str) -> str:
        if "properties" in schema:
            return self.register(hint, schema)

        # A map: its keys are values rather than field names, and the document says so.
        extra = schema.get("additionalProperties")

        if isinstance(extra, dict):
            return f"dict[str, {self.type_of(extra, f'{hint}Value')}]"

        return "dict[str, Any]"

    def register(self, hint: str, schema: dict[str, Any]) -> str:
        """One name per place a shape is used, and a suffix where two want the same one.

        Deduplicated within one operation and no further: dismissing an employee and writing a
        directory answer with the same keys, and naming one of them after the other is a method
        whose return type reads as somebody else's. The shapes the whole surface shares are
        components in the document, and those keep the names it gives them.
        """
        signature = (self.scope, json.dumps(schema, sort_keys=True))

        if signature in self.shapes:
            return self.shapes[signature]

        name = hint
        attempt = 2

        while name in self.blocks:
            name = f"{hint}{attempt}"
            attempt += 1

        self.blocks[name] = ""
        self.shapes[signature] = name
        self.blocks[name] = self.typed_dict(name, schema)

        return name

    def typed_dict(self, name: str, schema: dict[str, Any]) -> str:
        required = set(schema.get("required", []))
        properties: dict[str, Any] = schema.get("properties", {})

        if not properties:
            return f"{name} = dict[str, Any]\n"

        fields: dict[str, str] = {}

        for key, value in properties.items():
            child = self.type_of(value, self.child_hint(name, key))
            fields[key] = child if key in required else f"NotRequired[{child}]"

        # A payslip's period runs `from` a day `to` another, and neither word can be an attribute.
        # The call form takes any key; its types are quoted, since that form evaluates them and
        # `NotRequired` is imported for the checker alone.
        if any(not key.isidentifier() or keyword.iskeyword(key) for key in fields):
            entries = ", ".join(f'"{key}": "{annotation}"' for key, annotation in fields.items())

            return f'{name} = TypedDict("{name}", {{{entries}}})\n'

        lines = [f"class {name}(TypedDict):"]
        lines.extend(f"    {key}: {annotation}" for key, annotation in fields.items())

        return "\n".join(lines) + "\n"

    def child_hint(self, parent: str, key: str) -> str:
        """`UsersListResponse` plus `data` is `UsersListResponseData`, minus the noise."""
        for suffix in ("Response", "Body"):
            if parent.endswith(suffix):
                parent = parent[: -len(suffix)]

                break

        return f"{parent}{camel(key)}"

    def source(self) -> str:
        head = '''"""Every shape the Company API answers with or accepts, as TypedDicts.

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

'''

        names = ",\n".join(f'    "{name}"' for name in sorted(self.blocks))
        body = "\n\n".join(block.rstrip() for block in self.blocks.values())

        return f"{head}__all__ = [\n{names},\n]\n\n\n{body}\n"


class Operation:
    """One route, and everything the client needs to call it."""

    def __init__(self, path: str, method: str, spec: dict[str, Any], models: Models) -> None:
        self.path = path
        self.method = method
        self.spec = spec
        self.id: str = spec["operationId"]

        segments = OVERRIDES.get(self.id) or self.derived_segments()
        self.namespace = tuple(snake(part) for part in segments[:-1])
        self.name = snake(segments[-1])

        stem = camel("_".join(segments))
        models.scope = stem
        parameters = spec.get("parameters", [])

        self.path_params = [p["name"] for p in parameters if p["in"] == "path"]
        self.query = [p for p in parameters if p["in"] == "query"]
        self.idempotent = any(p["name"] == "Idempotency-Key" for p in parameters)

        self.status = "201" if "201" in spec["responses"] else "200"
        answer = spec["responses"][self.status].get("content", {}).get("application/json", {})
        self.returns = (
            models.type_of(answer["schema"], f"{stem}Response") if answer.get("schema") else "Any"
        )

        body = spec.get("requestBody", {}).get("content", {})
        self.multipart = "multipart/form-data" in body
        json_body = body.get("application/json", {}).get("schema")
        self.body = models.type_of(json_body, f"{stem}Body") if json_body else None
        self.form = body.get("multipart/form-data", {}).get("schema") if self.multipart else None
        self.models = models

    def derived_segments(self) -> tuple[str, ...]:
        parts = self.id.removeprefix(PREFIX).split(".")
        parts[-1] = VERBS.get(parts[-1], parts[-1])

        return tuple(parts)

    def signature(self, models: Models) -> list[str]:
        args = [f"{snake(name)}: int" for name in self.path_params]

        if self.body is not None:
            args.append(f"body: {self.body}")

        keyword_only = []

        if self.multipart and self.form is not None:
            # The bytes are what the call is about, so they go where a body would.
            args.append("file: bytes | IO[bytes]")
            keyword_only.append('filename: str = "upload"')

            for key, schema in self.form["properties"].items():
                if key == "file":
                    continue

                keyword_only.append(f"{snake(key)}: {models.type_of(schema, 'Any')} = None")

        for parameter in self.query:
            declared = models.type_of(parameter["schema"], camel(parameter["name"]))
            optional = declared if declared.endswith("| None") else f"{declared} | None"
            keyword_only.append(f"{snake(parameter['name'])}: {optional} = None")

        if self.idempotent:
            keyword_only.append("idempotency_key: str | None = None")

        return args + (["*", *keyword_only] if keyword_only else [])

    def docstring(self, indent: str) -> str:
        summary = self.spec.get("summary", self.name)
        description = (self.spec.get("description") or "").strip()
        lines = [f'{indent}"""{summary}']

        if description:
            lines.append("")
            lines.extend(f"{indent}{line}".rstrip() for line in description.splitlines())

        lines.append(f'{indent}"""')

        return "\n".join(lines)

    def call(self, indent: str, prefix: str) -> str:
        url = re.sub(r"\{(\w+)\}", lambda m: f"{{{snake(m.group(1))}}}", self.path)
        target = f'f"{url}"' if self.path_params else f'"{url}"'
        parts = [f'"{self.method.upper()}"', target]

        if self.query:
            pairs = ", ".join(f'"{p["name"]}": {snake(p["name"])}' for p in self.query)
            parts.append(f"query={{{pairs}}}")

        if self.body is not None:
            parts.append("json=body")

        if self.multipart and self.form is not None:
            others = [key for key in self.form["properties"] if key != "file"]
            data = ", ".join(f'"{key}": {snake(key)}' for key in others)
            parts.append('files={"file": (filename, file)}')

            if data:
                parts.append(f"data={{{data}}}")

        if self.idempotent:
            parts.append("idempotency_key=idempotency_key")

        arguments = ",\n".join(f"{indent}        {part}" for part in parts)

        # Cast rather than checked: nothing here validates, and the type is what the document says
        # the API answers with rather than something this package confirmed.
        return (
            f"{indent}return cast(\n"
            f"{indent}    {self.returns},\n"
            f"{indent}    {prefix}self._transport.request(\n{arguments},\n{indent}    ),\n"
            f"{indent})"
        )


def namespaces(operations: list[Operation]) -> dict[tuple[str, ...], list[Operation]]:
    tree: dict[tuple[str, ...], list[Operation]] = {(): []}

    for operation in operations:
        tree.setdefault(operation.namespace, [])

        for depth in range(1, len(operation.namespace)):
            tree.setdefault(operation.namespace[:depth], [])

        tree[operation.namespace].append(operation)

    return tree


def class_name(path: tuple[str, ...], is_async: bool) -> str:
    """The root is private: the client a caller constructs is hand-written and extends it."""
    if not path:
        return "_AsyncClocksterApi" if is_async else "_ClocksterApi"

    stem = camel("_".join(path))

    return f"Async{stem}" if is_async else stem


def render_namespace(
    path: tuple[str, ...],
    tree: dict[tuple[str, ...], list[Operation]],
    models: Models,
    is_async: bool,
) -> str:
    children = sorted(
        other for other in tree if len(other) == len(path) + 1 and other[: len(path)] == path
    )
    base = "_AsyncNamespace" if is_async else "_Namespace"
    lines = [f"class {class_name(path, is_async)}({base}):"]

    if path:
        lines.append(f'    """`clockster.{".".join(path)}`."""')
        lines.append("")

    if children:
        held = "_AsyncTransport" if is_async else "_SyncTransport"
        lines.append(f"    def __init__(self, transport: {held}) -> None:")
        lines.append("        super().__init__(transport)")

        for child in children:
            lines.append(f"        self.{child[-1]} = {class_name(child, is_async)}(transport)")

        lines.append("")

    for operation in tree[path]:
        arguments = ", ".join(["self", *operation.signature(models)])
        keyword = "async def" if is_async else "def"
        lines.append(f"    {keyword} {operation.name}({arguments}) -> {operation.returns}:")
        lines.append(operation.docstring("        "))
        lines.append(operation.call("        ", "await " if is_async else ""))
        lines.append("")

    if len(lines) == 1:
        lines.append("    pass")

    return "\n".join(lines).rstrip() + "\n"


def render_api(operations: list[Operation], models: Models) -> str:
    tree = namespaces(operations)
    order = sorted((path for path in tree if path), key=lambda path: (-len(path), path))
    head = '''"""The operations of the Company API, as they are called.

Generated from openapi/company-v3.json — see scripts/generate.py. Every method answers the parsed
body of the response; a refusal is raised rather than returned, so there is no branch between the
call and the rows.
"""

from __future__ import annotations

from typing import IO, Any, Literal, cast

from .._transport import _AsyncNamespace, _AsyncTransport, _Namespace, _SyncTransport
from .models import *  # noqa: F403 - the answer types, by the names the document gives them

'''
    blocks = []

    for is_async in (False, True):
        for path in order:
            blocks.append(render_namespace(path, tree, models, is_async))

        blocks.append(render_namespace((), tree, models, is_async))

    return head + "\n\n".join(blocks)


def main() -> int:
    document = json.loads(SPEC.read_text())
    models = Models(document)

    # Every component, whether or not an answer points at one: the refusal envelopes are named in
    # the document and typed nowhere else, and a caller reading `error.errors` wants the name.
    for component in document.get("components", {}).get("schemas", {}):
        models.component(f"#/components/schemas/{component}")

    operations = [
        Operation(path, method, spec, models)
        for path, item in document["paths"].items()
        for method, spec in item.items()
    ]
    operations.sort(key=lambda operation: (operation.namespace, operation.name))

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "__init__.py").write_text(
        '"""Generated from the specification; do not edit by hand."""\n'
    )
    (OUT / "models.py").write_text(models.source())
    (OUT / "api.py").write_text(render_api(operations, models))

    print(f"{len(operations)} operations, {len(models.blocks)} shapes.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
