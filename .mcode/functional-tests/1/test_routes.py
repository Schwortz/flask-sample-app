import os
import requests

BASE = "http://localhost:" + os.environ.get("PORT", "5000")


def test_hello():
    r = requests.get(BASE + "/", timeout=5)
    assert r.status_code == 200
    assert r.text == "Hello, Flask!"


def test_get_items():
    r = requests.get(BASE + "/items", timeout=5)
    assert r.status_code == 200
    assert isinstance(r.json()["items"], list)


def test_add_and_get_item():
    r = requests.post(BASE + "/items", json={"name": "ftrun"}, timeout=5)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    items = requests.get(BASE + "/items", timeout=5).json()["items"]
    idx = len(items) - 1
    g = requests.get(BASE + "/items/%d" % idx, timeout=5)
    assert g.status_code == 200
    assert g.json() == {"item": {"name": "ftrun"}}


def test_item_not_found():
    r = requests.get(BASE + "/items/99999", timeout=5)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}
