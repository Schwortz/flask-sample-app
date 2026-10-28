import os, requests
BASE = f"http://localhost:{os.environ.get('PORT', '5001')}"

def test_root_unchanged():
    r = requests.get(BASE + "/", timeout=10)
    assert r.status_code == 200 and r.text == "Hello, Flask!"

def test_items_list_unchanged():
    r = requests.get(BASE + "/items", timeout=10)
    assert r.status_code == 200 and "items" in r.json()

def test_item_not_found_unchanged():
    assert requests.get(BASE + "/items/99999", timeout=10).status_code == 404
