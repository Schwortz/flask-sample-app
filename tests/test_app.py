# tests/test_app.py
"""Unit tests for the Flask sample application routes using the test client."""

import unittest
from app import app

class TestAppRoutes(unittest.TestCase):
    """Test cases exercising the application routes via the Flask test client."""

    def setUp(self) -> None:
        """Create a test client for each test."""
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_route(self) -> None:
        """Verify ``GET /`` returns 200 and the greeting text."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, Flask!")

    def test_add_item_route(self) -> None:
        """Verify ``POST /items`` returns 201 and a success message."""
        response = self.app.post('/items', json={"name": "item1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {'message': 'Item added successfully'})

    def test_get_item_route(self) -> None:
        """Verify ``GET /items/0`` returns 200 and the stored item."""
        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'item': {'name': 'item1'}})

    def test_get_nonexistent_item_route(self) -> None:
        """Verify ``GET /items/1`` returns 404 with an error message."""
        response = self.app.get('/items/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

if __name__ == '__main__':
    unittest.main()
