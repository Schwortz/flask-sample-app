# tests/test_app.py

import unittest

from fastapi.testclient import TestClient

from app import app, routes


class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.app = TestClient(app)
        routes.items.clear()

    def test_hello_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello, Flask!")

    def test_add_item_route(self):
        response = self.app.post('/items', json={"name": "item1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'Item added successfully'})

    def test_get_item_route(self):
        self.app.post('/items', json={"name": "item1"})
        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'item': {'name': 'item1'}})

    def test_get_nonexistent_item_route(self):
        response = self.app.get('/items/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Item not found'})

    def test_get_items_route_empty(self):
        response = self.app.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'items': []})

    def test_get_items_route_after_add(self):
        self.app.post('/items', json={"name": "item1"})
        response = self.app.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'items': [{'name': 'item1'}]})

    def test_get_item_non_int_id_is_404(self):
        response = self.app.get('/items/abc')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Not Found'})

    def test_get_item_negative_id_is_404(self):
        self.app.post('/items', json={"name": "item1"})
        response = self.app.get('/items/-1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Item not found'})

    def test_add_item_invalid_body_is_422(self):
        response = self.app.post('/items', json=["not", "a", "dict"])
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'error': 'Invalid request body'})

    def test_unknown_route_is_404(self):
        response = self.app.get('/nope')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Not Found'})

if __name__ == '__main__':
    unittest.main()
