# tests/test_app.py

import unittest
from app import app

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        """Create a Flask test client for each test."""
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_route(self):
        """Verify the root route returns the greeting."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, Flask!")

    def test_add_item_route(self):
        """Verify adding an item returns 201."""
        response = self.app.post('/items', json={"name": "item1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {'message': 'Item added successfully'})

    def test_get_item_route(self):
        """Verify an existing item can be retrieved by index."""
        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'item': {'name': 'item1'}})

    def test_get_nonexistent_item_route(self):
        """Verify a missing item returns 404."""
        response = self.app.get('/items/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

if __name__ == '__main__':
    unittest.main()
