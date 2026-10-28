# app/routes.py
"""HTTP routes for the Flask sample application.

Provides a greeting endpoint and a simple in-memory item store exposed
through a small JSON API.

Attributes:
    items: In-memory list of items added through ``POST /items``.
"""

from typing import Any

from app import app
from flask import request
from flask.typing import ResponseReturnValue

items: list[dict[str, Any]] = []

@app.route('/')
def hello() -> ResponseReturnValue:
    """Return a greeting.

    Returns:
        ResponseReturnValue: The plain text ``"Hello, Flask!"`` with
        HTTP status 200 (OK).
    """
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items() -> ResponseReturnValue:
    """List all stored items.

    Returns:
        ResponseReturnValue: JSON ``{"items": [...]}`` with HTTP status
        200 (OK).
    """
    return {'items': items}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int) -> ResponseReturnValue:
    """Fetch a single item by its list index.

    Args:
        item_id: Zero-based index of the item in the store.

    Returns:
        ResponseReturnValue: One of:
            - 200 (OK): JSON ``{"item": {...}}`` when the item exists.
            - 404 (Not Found): JSON ``{"error": "Item not found"}`` when
              the index is out of range.
    """
    if item_id < len(items):
        return {'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item() -> ResponseReturnValue:
    """Add a new item from the JSON request body.

    Returns:
        ResponseReturnValue: JSON ``{"message": "Item added successfully"}``
        with HTTP status 201 (Created).
    """
    item = request.get_json()
    items.append(item)
    return {'message': 'Item added successfully'}, 201
