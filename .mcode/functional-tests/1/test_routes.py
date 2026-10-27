import requests

BASE = "http://localhost:5001"


def test_root_greeting():
    r = requests.get(f"{BASE}/", timeout=10)
    assert r.status_code == 200
    assert r.text == "Hello, Flask!"


def test_add_list_get_item():
    item = {"name": "ftrun_widget", "price": 3}
    r = requests.post(f"{BASE}/items", json=item, timeout=10)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    items = requests.get(f"{BASE}/items", timeout=10)
    assert items.status_code == 200
    lst = items.json()["items"]
    assert item in lst
    idx = lst.index(item)
    g = requests.get(f"{BASE}/items/{idx}", timeout=10)
    assert g.status_code == 200
    assert g.json() == {"item": item}


def test_get_item_not_found():
    r = requests.get(f"{BASE}/items/99999", timeout=10)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}
