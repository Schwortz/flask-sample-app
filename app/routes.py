# app/routes.py

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

router = APIRouter()

items = []


@router.get('/', response_class=HTMLResponse)
def hello():
    return "Hello, Flask!"


@router.get('/items')
def get_items():
    return {'items': items}


@router.get('/items/{item_id}')
def get_item(item_id: int):
    # Flask's int converter never matched negatives; keep them a 404.
    if 0 <= item_id < len(items):
        return {'item': items[item_id]}
    return JSONResponse({'error': 'Item not found'}, status_code=404)


@router.post('/items', status_code=201)
def add_item(item: dict):
    items.append(item)
    return {'message': 'Item added successfully'}
