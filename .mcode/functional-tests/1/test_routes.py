import os
import requests

BASE = f"http://localhost:{os.environ.get('PORT', '5001')}"


def test_get_root():
    r = requests.get(f"{BASE}/", timeout=10)
    assert r.status_code == 200
    assert r.text == "Hello, Flask!"


def test_get_items_list():
    r = requests.get(f"{BASE}/items", timeout=10)
    assert r.status_code == 200
    assert isinstance(r.json()["items"], list)


def test_post_item_and_get_item():
    before = len(requests.get(f"{BASE}/items", timeout=10).json()["items"])
    payload = {"name": "ftrun_widget"}
    r = requests.post(f"{BASE}/items", json=payload, timeout=10)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    items = requests.get(f"{BASE}/items", timeout=10).json()["items"]
    assert len(items) == before + 1
    r = requests.get(f"{BASE}/items/{before}", timeout=10)
    assert r.status_code == 200
    assert r.json() == {"item": payload}


def test_get_item_not_found():
    r = requests.get(f"{BASE}/items/999999", timeout=10)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}
