import unittest
from app import app, db, NameNumber

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Create an in-memory database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Cleanup the in-memory database
        with app.app_context():
            db.drop_all()

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

    def test_previous_entries(self):
        with app.app_context():
            new_entry1 = NameNumber(name='Alice', number='12345')
            new_entry2 = NameNumber(name='Bob', number='67890')
            db.session.add(new_entry1)
            db.session.add(new_entry2)
            db.session.commit()

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, Alice! Your number is 12345.', response.data)
        self.assertIn(b'Hello, Bob! Your number is 67890.', response.data)

if __name__ == '__main__':
    unittest.main()
