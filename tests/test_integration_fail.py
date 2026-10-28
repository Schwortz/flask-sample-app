"""Integration tests including a deliberately failing test."""

import requests  # type: ignore[import-untyped]  # types-requests not in requirements
import threading
from app import app


def test_that_always_fails(base_url: str) -> None:
    """Fail unconditionally to exercise failure reporting."""
    assert False

