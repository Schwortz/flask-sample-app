import os, uuid
import requests

BASE = f"http://localhost:{os.environ.get('PORT', '5001')}"
T = 10


def test_hello():
    r = requests.get(f"{BASE}/", timeout=T)
    assert r.status_code == 200
    assert r.text == "Hello, Flask!"
    assert r.headers["Content-Type"].startswith("text/html")


def test_get_items_json():
    r = requests.get(f"{BASE}/items", timeout=T)
    assert r.status_code == 200
    assert r.headers["Content-Type"].startswith("application/json")
    assert isinstance(r.json()["items"], list)


def test_add_and_get_item():
    tag = "ft_" + uuid.uuid4().hex
    before = requests.get(f"{BASE}/items", timeout=T).json()["items"]
    r = requests.post(f"{BASE}/items", json={"name": tag}, timeout=T)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    after = requests.get(f"{BASE}/items", timeout=T).json()["items"]
    assert len(after) == len(before) + 1
    assert after[-1] == {"name": tag}
    g = requests.get(f"{BASE}/items/{len(after) - 1}", timeout=T)
    assert g.status_code == 200
    assert g.headers["Content-Type"].startswith("application/json")
    assert g.json() == {"item": {"name": tag}}


def test_item_not_found():
    n = len(requests.get(f"{BASE}/items", timeout=T).json()["items"])
    r = requests.get(f"{BASE}/items/{n + 1000}", timeout=T)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}


def test_negative_id():
    r = requests.get(f"{BASE}/items/-1", timeout=T)
    assert r.status_code == 404
