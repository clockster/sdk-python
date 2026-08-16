"""This package's version, read once: its own `__version__` and the one in the User-Agent."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("clockster")
except PackageNotFoundError:  # pragma: no cover - a source tree nobody installed
    __version__ = "0.0.0"
