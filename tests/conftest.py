from collections.abc import Iterator
from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import TestingConfig


def close_app_handlers(app: Flask) -> None:
    """Close and detach every handler on the app logger (it is process-global)."""
    for handler in list(app.logger.handlers):
        handler.close()
        app.logger.removeHandler(handler)


@pytest.fixture
def app(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Flask]:
    monkeypatch.setenv("LOG_DIR", str(tmp_path / "logs"))
    flask_app = create_app(TestingConfig)
    yield flask_app
    close_app_handlers(flask_app)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
