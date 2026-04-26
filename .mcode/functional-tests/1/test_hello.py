"""Functional test for GET / on the flask-sample-app (origin).

Same assertions as the target test — used to establish the behavioral
baseline for Milestone 1 of the Flask -> Go migration.
"""

import os

import pytest
import requests

PORT = os.environ.get("PORT", "5001")
BASE_URL = f"http://127.0.0.1:{PORT}"


@pytest.fixture(autouse=True)
def health_check():
    """Confirm the app is reachable on the configured port before each test."""
    resp = requests.get(f"{BASE_URL}/", timeout=5)
    assert resp.status_code == 200, (
        f"App not reachable at {BASE_URL}/ (got {resp.status_code})"
    )


class TestHelloRoute:
    """GET / — the hello endpoint."""

    def test_hello_returns_200(self):
        """HAPPY_PATH: GET / returns HTTP 200."""
        resp = requests.get(f"{BASE_URL}/", timeout=5)
        assert resp.status_code == 200

    def test_hello_body_exact_text(self):
        """HAPPY_PATH: GET / body equals exactly 'Hello, Flask!'."""
        resp = requests.get(f"{BASE_URL}/", timeout=5)
        assert resp.text == "Hello, Flask!", (
            f"Expected body 'Hello, Flask!', got {resp.text!r}"
        )

    def test_hello_content_type(self):
        """HAPPY_PATH: GET / returns Content-Type 'text/html; charset=utf-8'."""
        resp = requests.get(f"{BASE_URL}/", timeout=5)
        ct = resp.headers.get("Content-Type", "")
        assert ct == "text/html; charset=utf-8", (
            f"Expected Content-Type 'text/html; charset=utf-8', got {ct!r}"
        )


class TestHelloRouteNegative:
    """Negative cases for GET /."""

    def test_unknown_route_returns_404(self):
        """NOT_FOUND: GET /does-not-exist returns 404."""
        resp = requests.get(f"{BASE_URL}/does-not-exist", timeout=5)
        assert resp.status_code == 404

    def test_post_to_root_not_allowed(self):
        """INVALID_INPUT: POST / is not registered; expect 4xx (404 or 405)."""
        resp = requests.post(f"{BASE_URL}/", json={}, timeout=5)
        assert 400 <= resp.status_code < 500, (
            f"Expected 4xx for POST /, got {resp.status_code}"
        )
