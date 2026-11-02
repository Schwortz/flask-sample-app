"""Blueprint with the items REST API."""

import re
from typing import Any, cast

from flask import Blueprint, current_app, request
from flask.typing import ResponseReturnValue
from werkzeug.exceptions import BadRequest, NotFound

bp = Blueprint("main", __name__)

_NEGATIVE_INT = re.compile(r"-[0-9]+")


def _items() -> list[Any]:
    return cast("list[Any]", current_app.extensions["items"])


@bp.errorhandler(BadRequest)
def handle_bad_request(error: BadRequest) -> ResponseReturnValue:
    return {"error": error.description or "Bad request"}, 400


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
    """Negative ids are rejected with 400; other non-int ids stay 404 as in origin."""
    if _NEGATIVE_INT.fullmatch(item_id):
        return {"error": "Invalid item id"}, 400
    raise NotFound()


@bp.route("/items", methods=["POST"])
def add_item() -> ResponseReturnValue:
    if not request.is_json:
        raise BadRequest("Invalid JSON body")
    try:
        item = request.get_json()
    except BadRequest as exc:
        raise BadRequest("Invalid JSON body") from exc
    _items().append(item)
    return {"message": "Item added successfully"}, 201
