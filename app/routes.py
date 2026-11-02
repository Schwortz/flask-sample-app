# app/routes.py
from __future__ import annotations

from typing import Any, Union

from app import app
from flask import request

items: list[Any] = []

@app.route('/')
def hello() -> str:
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items() -> dict[str, list[Any]]:
    return {'items': items}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int) -> Union[dict[str, Any], tuple[dict[str, Any], int]]:
    if item_id < len(items):
        return {'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item() -> tuple[dict[str, Any], int]:
    item = request.get_json()
    items.append(item)
    return {'message': 'Item added successfully'}, 201
