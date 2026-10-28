import os, requests
B = f"http://localhost:{os.environ.get('PORT','5001')}"

def test_health():
    r = requests.get(B+"/health", timeout=5)
    assert r.status_code == 200 and r.json() == {"status": "ok"}

def test_root():
    r = requests.get(B+"/", timeout=5)
    assert r.status_code == 200 and r.text == "Hello, Flask!"

def test_items_flow():
    r = requests.get(B+"/items", timeout=5)
    assert r.status_code == 200
    n = len(r.json()["items"])
    r = requests.post(B+"/items", json={"name": "ftrun_x"}, timeout=5)
    assert r.status_code == 201 and r.json() == {"message": "Item added successfully"}
    r = requests.get(B+f"/items/{n}", timeout=5)
    assert r.status_code == 200 and r.json() == {"item": {"name": "ftrun_x"}}

def test_item_not_found():
    r = requests.get(B+"/items/99999", timeout=5)
    assert r.status_code == 404 and r.json() == {"error": "Item not found"}
