import os, requests
B = f"http://localhost:{os.environ.get('PORT','5001')}"

def test_health_get():
    r = requests.get(B+"/health", timeout=5)
    assert r.status_code == 200 and r.json() == {"status": "ok"}

def test_health_post_405():
    assert requests.post(B+"/health", timeout=5).status_code == 405

def test_root():
    r = requests.get(B+"/", timeout=5)
    assert r.status_code == 200 and r.text == "Hello, Flask!"

def test_items_flow():
    r = requests.get(B+"/items", timeout=5)
    assert r.status_code == 200
    n = len(r.json()["items"])
    p = requests.post(B+"/items", json={"name": "ftrun_a"}, timeout=5)
    assert p.status_code == 201 and p.json() == {"message": "Item added successfully"}
    assert requests.get(B+"/items", timeout=5).json()["items"][n:] == [{"name": "ftrun_a"}]
    g = requests.get(f"{B}/items/{n}", timeout=5)
    assert g.status_code == 200 and g.json() == {"item": {"name": "ftrun_a"}}

def test_item_missing_404():
    r = requests.get(B+"/items/99999", timeout=5)
    assert r.status_code == 404 and r.json() == {"error": "Item not found"}
