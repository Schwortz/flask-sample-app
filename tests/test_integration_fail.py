"""Integration tests including a deliberately failing test."""

import requests  # type: ignore[import-untyped]  # types-requests not in requirements
import threading
from app import app


def test_hello_route(base_url: str) -> None:
    """Test the root endpoint returns correct greeting."""
    response = requests.get(f"{base_url}/")
    assert response.status_code == 200
    assert response.text == "Hello, Flask!"
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'


def test_that_always_fails(base_url: str) -> None:
    """Fail unconditionally to exercise failure reporting."""
    assert False

