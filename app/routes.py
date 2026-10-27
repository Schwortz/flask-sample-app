# app/routes.py

from app import app
from typing import Any

from flask import request
from flask.typing import ResponseReturnValue

items: list[dict[str, Any]] = []

@app.route('/')
def hello() -> ResponseReturnValue:
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items() -> ResponseReturnValue:
    return {'items': items}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int) -> ResponseReturnValue:
    if item_id < len(items):
        return {'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item() -> ResponseReturnValue:
    item = request.get_json()
    items.append(item)
    return {'message': 'Item added successfully'}, 201
