import os
import requests

BASE = f"http://localhost:{os.environ.get('PORT', '5001')}"


def test_root_hello():
    r = requests.get(f"{BASE}/", timeout=5)
    assert r.status_code == 200
    assert r.text == "Hello, Flask!"


def test_list_items():
    r = requests.get(f"{BASE}/items", timeout=5)
    assert r.status_code == 200
    assert isinstance(r.json()["items"], list)


def test_add_item_and_get_it():
    n = len(requests.get(f"{BASE}/items", timeout=5).json()["items"])
    payload = {"name": "ftrun_widget"}
    r = requests.post(f"{BASE}/items", json=payload, timeout=5)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    r = requests.get(f"{BASE}/items/{n}", timeout=5)
    assert r.status_code == 200
    assert r.json() == {"item": payload}


def test_get_item_not_found():
    r = requests.get(f"{BASE}/items/99999", timeout=5)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}


def test_get_item_non_int_404():
    r = requests.get(f"{BASE}/items/abc", timeout=5)
    assert r.status_code == 404
