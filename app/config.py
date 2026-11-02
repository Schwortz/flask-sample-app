"""Configuration classes with environment overrides."""

import os
from pathlib import Path


class Config:
    """Default configuration."""

    TESTING = False
    HOST = "127.0.0.1"
    PORT = 5001
    LOG_DIR = str(Path.home() / ".flask_sample_app")


class TestingConfig(Config):
    """Configuration used by the test suite."""

    TESTING = True


def env_overrides() -> dict[str, object]:
    """Read HOST, PORT and LOG_DIR overrides from the environment."""
    overrides: dict[str, object] = {}
    if "HOST" in os.environ:
        overrides["HOST"] = os.environ["HOST"]
    if "PORT" in os.environ:
        overrides["PORT"] = int(os.environ["PORT"])
    if "LOG_DIR" in os.environ:
        overrides["LOG_DIR"] = os.environ["LOG_DIR"]
    return overrides
