import os
import requests

BASE = f"http://localhost:{os.environ.get('PORT', '5001')}"


def test_health_ok():
    r = requests.get(f"{BASE}/health", timeout=10)
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_health_post_not_allowed():
    assert requests.post(f"{BASE}/health", timeout=10).status_code == 405


def test_root():
    r = requests.get(f"{BASE}/", timeout=10)
    assert r.status_code == 200 and r.text == "Hello, Flask!"


def test_items_create_and_list_and_get():
    r = requests.post(f"{BASE}/items", json={"name": "ftrun_a"}, timeout=10)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    items = requests.get(f"{BASE}/items", timeout=10)
    assert items.status_code == 200
    lst = items.json()["items"]
    assert {"name": "ftrun_a"} in lst
    idx = lst.index({"name": "ftrun_a"})
    g = requests.get(f"{BASE}/items/{idx}", timeout=10)
    assert g.status_code == 200 and g.json() == {"item": {"name": "ftrun_a"}}


def test_item_not_found():
    r = requests.get(f"{BASE}/items/99999", timeout=10)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}
