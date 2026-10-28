"""Shared pytest fixtures for the integration tests."""

import os
import time
from collections.abc import Iterator

import pytest
import requests  # type: ignore[import-untyped]  # types-requests not in requirements


@pytest.fixture(scope="session")
def base_url() -> Iterator[str]:
    """Wait for the Flask server to be ready and return the base URL.

    Yields:
        The base URL of the server under test.

    Raises:
        RuntimeError: If the server does not respond in time.
    """
    # Use a test port to avoid conflicts
    test_port = int(os.environ.get("TEST_PORT", 5001))
    base_url = f"http://localhost:{test_port}"

    # Wait for server to be ready
    max_attempts = 4
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
