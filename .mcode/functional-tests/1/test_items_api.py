import requests
B = "http://localhost:5001"
T = 10


def test_root_html():
    r = requests.get(B + "/", timeout=T)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert r.text == "Hello, Flask!"


def test_post_item_and_persist_order():
    before = requests.get(B + "/items", timeout=T).json()["items"]
    a = {"name": "ftrun_a", "n": 1}
    b = {"name": "ftrun_b"}
    for x in (a, b):
        r = requests.post(B + "/items", json=x, timeout=T)
        assert r.status_code == 201
        assert r.headers["content-type"].startswith("application/json")
        assert r.json() == {"message": "Item added successfully"}
    after = requests.get(B + "/items", timeout=T).json()["items"]
    assert after == before + [a, b]
    i = len(before)
    r = requests.get(f"{B}/items/{i}", timeout=T)
    assert r.status_code == 200 and r.json() == {"item": a}
    assert requests.get(f"{B}/items/{i+1}", timeout=T).json() == {"item": b}


def test_post_empty_object():
    r = requests.post(B + "/items", json={}, timeout=T)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}


def test_get_items_shape():
    r = requests.get(B + "/items", timeout=T)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/json")
    assert isinstance(r.json()["items"], list)


def test_item_out_of_range():
    n = len(requests.get(B + "/items", timeout=T).json()["items"])
    r = requests.get(f"{B}/items/{n+1000}", timeout=T)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}


def test_item_negative():
    r = requests.get(B + "/items/-1", timeout=T)
    assert r.status_code == 404


def test_item_non_int():
    assert requests.get(B + "/items/abc", timeout=T).status_code == 404


def test_post_non_object_422():
    for body in ([1, 2], "str", 5):
        r = requests.post(B + "/items", json=body, timeout=T)
        assert r.status_code == 422
        assert "error" in r.json()


def test_post_invalid_json_422():
    r = requests.post(B + "/items", data="{bad", headers={"Content-Type": "application/json"}, timeout=T)
    assert r.status_code == 422
    assert "error" in r.json()


def test_trailing_slash_get_404():
    r = requests.get(B + "/items/", timeout=T, allow_redirects=False)
    assert r.status_code == 404
    assert r.json() == {"error": "Not Found"}


def test_trailing_slash_post_404():
    r = requests.post(B + "/items/", json={"a": 1}, timeout=T, allow_redirects=False)
    assert r.status_code == 404
    assert r.json() == {"error": "Not Found"}
