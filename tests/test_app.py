from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import Config, TestingConfig


def test_hello(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Hello, Flask!"


def test_add_and_get_item(client: FlaskClient) -> None:
    response = client.post("/items", json={"name": "item1"})
    assert response.status_code == 201
    assert response.get_json() == {"message": "Item added successfully"}
    assert client.get("/items/0").get_json() == {"item": {"name": "item1"}}
    assert client.get("/items").get_json() == {"items": [{"name": "item1"}]}


def test_items_empty_with_isolated_state(client: FlaskClient) -> None:
    assert client.get("/items").get_json() == {"items": []}


def test_missing_item(client: FlaskClient) -> None:
    response = client.get("/items/1")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Item not found"}


def test_negative_id(client: FlaskClient) -> None:
    response = client.get("/items/-1")
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid item id"}


def test_invalid_json(client: FlaskClient) -> None:
    response = client.post("/items", data="{nope", content_type="application/json")
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid JSON body"}


def test_missing_body(client: FlaskClient) -> None:
    assert client.post("/items").status_code == 400


def test_config_env_overrides(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("HOST", "0.0.0.0")
    monkeypatch.setenv("PORT", "6000")
    monkeypatch.setenv("LOG_DIR", str(tmp_path))
    app = create_app(TestingConfig)
    assert app.config["HOST"] == "0.0.0.0"
    assert app.config["PORT"] == 6000
    assert app.config["LOG_DIR"] == str(tmp_path)
    assert app.config["TESTING"] is True
    _close(app)


def test_default_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("HOST", "PORT"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("LOG_DIR", str(tmp_path))
    app = create_app()
    assert app.config["HOST"] == Config.HOST == "127.0.0.1"
    assert app.config["PORT"] == 5001
    _close(app)


def test_logging_written_to_log_dir(app: Flask) -> None:
    log_file = Path(str(app.config["LOG_DIR"])) / "flask_sample_app.log"
    for handler in app.logger.handlers:
        handler.flush()
    assert "Application starting" in log_file.read_text()


def _close(app: Flask) -> None:
    for handler in list(app.logger.handlers):
        handler.close()
        app.logger.removeHandler(handler)


def test_create_app_twice_keeps_single_file_handler(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("LOG_DIR", str(tmp_path))
    create_app(TestingConfig)
    app = create_app(TestingConfig)
    handlers = [h for h in app.logger.handlers if isinstance(h, RotatingFileHandler)]
    assert len(handlers) == 1
    _close(app)


def test_non_integer_id_not_found(client: FlaskClient) -> None:
    assert client.get("/items/abc").status_code == 404


def test_json_null_body_accepted(client: FlaskClient) -> None:
    response = client.post("/items", data="null", content_type="application/json")
    assert response.status_code == 201
    assert client.get("/items").get_json() == {"items": [None]}
