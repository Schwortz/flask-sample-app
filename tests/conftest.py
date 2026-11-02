from collections.abc import Iterator
from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import TestingConfig


@pytest.fixture
def app(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Flask]:
    monkeypatch.setenv("LOG_DIR", str(tmp_path / "logs"))
    flask_app = create_app(TestingConfig)
    yield flask_app
    for handler in list(flask_app.logger.handlers):
        if handler.__class__.__name__ == "RotatingFileHandler":
            handler.close()
            flask_app.logger.removeHandler(handler)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
