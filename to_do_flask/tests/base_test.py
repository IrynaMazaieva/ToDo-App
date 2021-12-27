from unittest import TestCase
from to_do_flask import application


class BaseCase(TestCase):

    def setUp(self):
        SQLALCHEMY_DATABASE_URI = "sqlite:///./test.bd"
        self.app = application.create_app(SQLALCHEMY_DATABASE_URI)
        self.db = self.app.db

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all(app=self.app)
