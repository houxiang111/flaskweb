import unittest
from flask import current_app
from app import create_app,db

class BasicTest(unittest.TestCase):
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exist(self):
        self.assertFalse(current_app is None)

    def test_app_config(self):
        self.assertTrue(current_app.config['TESTING'])

    
