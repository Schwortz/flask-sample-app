# tests/test_integration.py
"""Integration tests including an intentionally failing test."""

from collections.abc import Iterator

import pytest
import requests
import threading
import time
import os
from app import app


@pytest.fixture(scope="session")
def base_url() -> Iterator[str]:
    """Wait for the running Flask server and provide its base URL.

    Yields:
        The base URL of the server, e.g. ``http://localhost:5001``.

    Raises:
        RuntimeError: If the server does not respond with 200 in time.
    """
    # Use a test port to avoid conflicts
    test_port: int = int(os.environ.get("TEST_PORT", 5001))
    base_url: str = f"http://localhost:{test_port}"
    
    # Wait for server to be ready
    max_attempts: int = 4
    for _ in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/", timeout=1)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(0.1)
    else:
        raise RuntimeError("Server failed to start within expected time")
    
    yield base_url


def test_hello_route(base_url: str) -> None:
    """Test the root endpoint returns correct greeting.

    Args:
        base_url: Base URL of the running server.
    """
    response = requests.get(f"{base_url}/")
    assert response.status_code == 200
    assert response.text == "Hello, Flask!"
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'


def test_that_always_fails(base_url: str) -> None:
    """Fail intentionally to validate failure reporting.

    Args:
        base_url: Base URL of the running server.

    Raises:
        AssertionError: Always.
    """
    assert False

