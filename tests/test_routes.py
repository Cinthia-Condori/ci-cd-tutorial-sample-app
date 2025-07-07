import os
import sys
import unittest
import json

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Menu

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DB = os.path.join(BASE_DIR, 'test.db')


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = \
            os.environ.get('TEST_DATABASE_URL') or \
            'sqlite:///' + TEST_DB
        self.app.config['TESTING'] = True

        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        body = json.loads(response.data)
        self.assertEqual(body['status'], 'ok')

    def test_menu_empty(self):
        response = self.client.get('/menu', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_menu_item(self):
        test_name = "test"
        with self.app.app_context():
            test_item = Menu(name=test_name)
            db.session.add(test_item)
            db.session.commit()
        response = self.client.get('/menu', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        body = json.loads(response.data)
        self.assertIn('today_special', body)
        self.assertEqual(body['today_special'], test_name)


if __name__ == "__main__":
    unittest.main()
