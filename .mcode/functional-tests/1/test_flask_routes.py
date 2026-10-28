import os, requests
BASE = f"http://localhost:{os.environ.get('PORT', '5001')}"

def test_root():
    r = requests.get(BASE + "/", timeout=10)
    assert r.status_code == 200 and r.text == "Hello, Flask!"

def test_add_and_get_item():
    r = requests.post(BASE + "/items", json={"name": "ftrun"}, timeout=10)
    assert r.status_code == 201
    assert r.json()["message"] == "Item added successfully"
    lst = requests.get(BASE + "/items", timeout=10)
    assert lst.status_code == 200 and {"name": "ftrun"} in lst.json()["items"]
    r = requests.get(BASE + "/items/0", timeout=10)
    assert r.status_code == 200 and "item" in r.json()

def test_item_not_found():
    r = requests.get(BASE + "/items/99999", timeout=10)
    assert r.status_code == 404
