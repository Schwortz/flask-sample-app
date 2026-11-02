"""Flask sample application package."""

import logging
import platform
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask

from app.config import Config, env_overrides

LOG_FILE_NAME = "flask_sample_app.log"
_HANDLER_MARKER = "_flask_sample_app"


def _configure_logging(app: Flask) -> None:
    log_dir = Path(str(app.config["LOG_DIR"]))
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / LOG_FILE_NAME

    # The "app" logger is process-global; replace our previous handler instead of stacking.
    for existing in list(app.logger.handlers):
        if getattr(existing, _HANDLER_MARKER, False):
            app.logger.removeHandler(existing)
            existing.close()

    handler = RotatingFileHandler(log_file, maxBytes=1_048_576, backupCount=5)
    setattr(handler, _HANDLER_MARKER, True)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info(
        "Application starting - host=%s, platform=%s, log_file=%s",
        platform.node(),
        platform.system(),
        log_file,
    )


def create_app(config: type[Config] | str | None = None) -> Flask:
    """Application factory.

    ``config`` may be a config class, a dotted import path, or None for the default.
    Environment overrides (HOST, PORT, LOG_DIR) are applied afterwards.
    """
    app = Flask(__name__)
    app.config.from_object(config if config is not None else Config)
    app.config.update(env_overrides())

    app.extensions["items"] = []

    from app.routes import bp

    app.register_blueprint(bp)
    _configure_logging(app)
    return app
