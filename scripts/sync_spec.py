"""Refresh openapi/company-v3.json from the deployment that implements it.

`--check` writes nothing and exits 1 on a difference, which is what CI runs.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

SOURCE = os.environ.get("CLOCKSTER_SPEC_URL", "https://api.clockster.com/openapi/v3.json")

TARGET = Path(__file__).resolve().parent.parent / "openapi" / "company-v3.json"


def main() -> int:
    check = "--check" in sys.argv

    with urllib.request.urlopen(SOURCE, timeout=60) as response:
        if response.status != 200:
            print(f"{SOURCE} answered {response.status}.", file=sys.stderr)

            return 1

        published = json.load(response)

    committed = json.loads(TARGET.read_text()) if TARGET.is_file() else None

    # Compared as documents rather than as text: the builder writes four-space indentation and this
    # writes two, and that difference is not drift.
    if committed == published:
        print("Specification is current.")

        return 0

    if check:
        print(
            f"Specification has drifted from {SOURCE}. Run `make spec generate`.", file=sys.stderr
        )

        return 1

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(published, indent=2, ensure_ascii=False) + "\n")
    print("Specification updated. Run `make generate`.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
