"""The shapes of what this API answers with and accepts, by the names the document gives them.

    from clockster.models import UsersListRow

They are TypedDicts: a type checker sees the fields, and what a method answers is a plain
dictionary.
"""

from __future__ import annotations

from ._generated.models import *  # noqa: F403
from ._generated.models import __all__ as __all__
