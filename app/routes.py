"""Blueprint with the items REST API."""

from typing import Any, cast

from flask import Blueprint, current_app, request
from flask.typing import ResponseReturnValue
from werkzeug.exceptions import BadRequest

bp = Blueprint("main", __name__)


def _items() -> list[Any]:
    return cast("list[Any]", current_app.extensions["items"])


@bp.errorhandler(BadRequest)
def handle_bad_request(error: BadRequest) -> ResponseReturnValue:
    return {"error": "Invalid JSON body"}, 400


@bp.route("/")
def hello() -> ResponseReturnValue:
    return "Hello, Flask!"


@bp.route("/items", methods=["GET"])
def get_items() -> ResponseReturnValue:
    return {"items": _items()}


@bp.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id: int) -> ResponseReturnValue:
    items = _items()
    if item_id < len(items):
        return {"item": items[item_id]}
    return {"error": "Item not found"}, 404


@bp.route("/items/<item_id>", methods=["GET"])
def get_item_invalid(item_id: str) -> ResponseReturnValue:
    """Negative or non-integer ids (the int converter rejects them)."""
    return {"error": "Invalid item id"}, 400


@bp.route("/items", methods=["POST"])
def add_item() -> ResponseReturnValue:
    item = request.get_json(silent=True)
    if item is None:
        raise BadRequest("Invalid JSON body")
    _items().append(item)
    return {"message": "Item added successfully"}, 201
