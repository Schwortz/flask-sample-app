# tests/test_app.py

import unittest

from fastapi.testclient import TestClient

from app import app


class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.app = TestClient(app)

    def test_hello_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello, Flask!")

    def test_add_item_route(self):
        response = self.app.post('/items', json={"name": "item1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'Item added successfully'})

    def test_get_item_route(self):
        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'item': {'name': 'item1'}})

    def test_get_nonexistent_item_route(self):
        response = self.app.get('/items/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Item not found'})

if __name__ == '__main__':
    unittest.main()
