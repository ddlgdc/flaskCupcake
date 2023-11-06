import unittest
from flask import Flask
from models import db, Cupcake
from app import app

class CupcakeViewsTestCase(unittest.TestCase):
    """Tests for views of API."""

    def setUp(self):
        self.app = app.test_client()

    def test_list_cupcakes(self):
        response = self.app.get("/api/cupcakes")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('cupcakes', data)

    def test_get_cupcake(self):
        response = self.app.get('/api/cupcakes/1')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('cupcake', data)

    def test_get_cupcake_not_found(self):
        response = self.app.get('/api/cupcakes/999')
        self.assertEqual(response.status_code, 404)

    def test_create_cupcake(self):
        data = {
            'flavor': 'vanilla',
            'size': 'medium',
            'rating': 8.5,
            'image': 'https://example.com/cupcake.jpg'
        }

        response = self.app.post('/api/cupcakes', json=data)
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn('cupcake', data)


if __name__ == '__main__':
    unittest.main()
