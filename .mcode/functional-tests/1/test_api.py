import os
import requests

BASE = f"http://localhost:{os.environ.get('PORT', '5001')}"


def test_root():
    r = requests.get(BASE + "/", timeout=10)
    assert r.status_code == 200
    assert r.text == "Hello, Flask!"


def test_list_items():
    r = requests.get(BASE + "/items", timeout=10)
    assert r.status_code == 200
    assert isinstance(r.json()["items"], list)


def test_post_and_get_item():
    payload = {"name": "ftrun_widget"}
    r = requests.post(BASE + "/items", json=payload, timeout=10)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    items = requests.get(BASE + "/items", timeout=10).json()["items"]
    idx = items.index(payload)
    r = requests.get(f"{BASE}/items/{idx}", timeout=10)
    assert r.status_code == 200
    assert r.json() == {"item": payload}


def test_item_not_found():
    r = requests.get(BASE + "/items/99999", timeout=10)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}
