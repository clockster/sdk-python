"""Every operation in the specification must be reachable on the client.

A naming scheme that shortens method names can collapse two operations onto one silently, and a
namespace nothing reaches would pass a count that only added methods up.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "src"))

from clockster import AsyncClockster, Clockster  # noqa: E402
from clockster._transport import _AsyncNamespace, _Namespace  # noqa: E402

VERBS = {"get", "post", "put", "patch", "delete"}

GENERATED = "clockster._generated.api"


def reachable(namespace: Any, prefix: str) -> list[str]:
    """Walked from the root rather than counted: a container nothing reaches is not covered."""
    found: list[str] = []

    # dir() rather than the instance dictionary: the root's own operations are inherited from the
    # generated class the hand-written client extends.
    for name in sorted(dir(namespace)):
        if name.startswith("_"):
            continue

        value = getattr(namespace, name)

        if isinstance(value, _Namespace | _AsyncNamespace):
            found.extend(reachable(value, f"{prefix}.{name}"))
        elif callable(value) and getattr(value, "__module__", "") == GENERATED:
            found.append(f"{prefix}.{name}()")

    return found


def main() -> int:
    document = json.loads((ROOT / "openapi" / "company-v3.json").read_text())
    operations = sum(len(VERBS & set(item)) for item in document["paths"].values())

    for client, label in ((Clockster("x"), "clockster"), (AsyncClockster("x"), "async clockster")):
        found = reachable(client, label)

        if len(found) != operations:
            print(
                f"{operations} operations in the specification, {len(found)} reachable on the "
                f"{label}. Two operations whose names collide are silently merged; check OVERRIDES "
                "in scripts/generate.py.",
                file=sys.stderr,
            )

            return 1

    print(f"{operations} operations, all reachable, blocking and awaited.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
