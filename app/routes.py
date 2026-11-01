# app/routes.py

"""HTTP routes for the sample items API."""

from typing import Any

from app import app
from flask import request

items: list[Any] = []

@app.route('/')
def hello() -> str:
    """Return a greeting.

    Returns:
        The plain-text greeting "Hello, Flask!".
    """
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items() -> dict[str, list[Any]]:
    """List all stored items.

    Returns:
        A JSON object of the form ``{"items": [...]}``.
    """
    return {'items': items}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int) -> dict[str, Any] | tuple[dict[str, str], int]:
    """Fetch a single item by its index.

    Args:
        item_id: Zero-based index of the item in the item list.

    Returns:
        ``{"item": <item>}`` if the index exists; otherwise a tuple of
        ``{"error": "Item not found"}`` and the HTTP status 404.
    """
    if item_id < len(items):
        return {'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item() -> tuple[dict[str, str], int]:
    """Append the JSON request body to the item list.

    Returns:
        A tuple of a confirmation message and the HTTP status 201.
    """
    item = request.get_json()
    items.append(item)
    return {'message': 'Item added successfully'}, 201
