import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enter Names and Numbers', response.data)

    def test_greet_single(self):
        response = self.app.post('/greet', data=dict(names='Alice', numbers='12345'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, Alice! Your number is 12345.', response.data)

    def test_greet_multiple(self):
        response = self.app.post('/greet', data=dict(names='Alice,Bob', numbers='12345,67890'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, Alice! Your number is 12345.', response.data)
        self.assertIn(b'Hello, Bob! Your number is 67890.', response.data)

    def test_greet_mismatch(self):
        response = self.app.post('/greet', data=dict(names='Alice', numbers='12345,67890'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error: The number of names and numbers must be equal.', response.data)

if __name__ == '__main__':
    unittest.main()
