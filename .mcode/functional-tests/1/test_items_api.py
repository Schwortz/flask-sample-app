import requests
import pytest

BASE = "http://localhost:5001"


@pytest.fixture(autouse=True, scope="module")
def _up():
    r = requests.get(BASE + "/", timeout=5)
    assert r.status_code == 200


def test_root_greeting():
    r = requests.get(BASE + "/", timeout=5)
    assert r.status_code == 200
    assert r.text == "Hello, Flask!"


def test_list_items_shape():
    r = requests.get(BASE + "/items", timeout=5)
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body["items"], list)


def test_create_then_get_and_list():
    before = requests.get(BASE + "/items", timeout=5).json()["items"]
    payload = {"name": "ftrun_widget", "qty": 3}
    r = requests.post(BASE + "/items", json=payload, timeout=5)
    assert r.status_code == 201
    assert r.json() == {"message": "Item added successfully"}
    after = requests.get(BASE + "/items", timeout=5).json()["items"]
    assert len(after) == len(before) + 1
    assert after[-1] == payload
    r = requests.get(f"{BASE}/items/{len(after) - 1}", timeout=5)
    assert r.status_code == 200
    assert r.json() == {"item": payload}


def test_get_item_not_found():
    r = requests.get(BASE + "/items/999999", timeout=5)
    assert r.status_code == 404
    assert r.json() == {"error": "Item not found"}


def test_get_item_non_int_id_404():
    r = requests.get(BASE + "/items/abc", timeout=5)
    assert r.status_code == 404


def test_post_non_json_rejected():
    r = requests.post(BASE + "/items", data="not json", headers={"Content-Type": "text/plain"}, timeout=5)
    assert r.status_code in (400, 415)


def test_post_malformed_json_400():
    r = requests.post(BASE + "/items", data="{bad", headers={"Content-Type": "application/json"}, timeout=5)
    assert r.status_code == 400


def test_method_not_allowed_delete():
    r = requests.delete(BASE + "/items", timeout=5)
    assert r.status_code == 405


def test_unknown_route_404():
    assert requests.get(BASE + "/nope", timeout=5).status_code == 404
