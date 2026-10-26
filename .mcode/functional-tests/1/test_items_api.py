import os
import uuid

import requests

BASE = f"http://localhost:{os.environ.get('PORT', '5001')}"


def test_root():
    r = requests.get(f"{BASE}/", timeout=10)
    assert r.status_code == 200
    assert r.text == "Hello, Flask!"


def test_list_items():
    r = requests.get(f"{BASE}/items", timeout=10)
    assert r.status_code == 200
    assert isinstance(r.json()["items"], list)


def test_add_then_fetch_item():
    name = f"ftrun_{uuid.uuid4().hex[:8]}"
    before = requests.get(f"{BASE}/items", timeout=10).json()["items"]
    r = requests.post(f"{BASE}/items", json={"name": name, "price": 3}, timeout=10)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    idx = len(before)
    g = requests.get(f"{BASE}/items/{idx}", timeout=10)
    assert g.status_code == 200
    assert g.json() == {"item": {"name": name, "price": 3}}
    assert {"name": name, "price": 3} in requests.get(f"{BASE}/items", timeout=10).json()["items"]


def test_item_not_found():
    r = requests.get(f"{BASE}/items/999999", timeout=10)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}


def test_item_non_int_id():
    r = requests.get(f"{BASE}/items/abc", timeout=10)
    assert r.status_code == 404
