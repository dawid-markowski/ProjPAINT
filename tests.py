import os
os.environ['DATABASE_URL'] = 'sqlite://'

import unittest
from app import db,create_app
from app.models import User, Part, Comment, Cart, CartItem, Order
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='jurek', email='jurek@wp.pl')
        u.set_password('drogie_maslo')
        self.assertFalse(u.check_password('kakakka'))
        self.assertTrue(u.check_password('drogie_maslo'))
        u1 = User(username='basia', email='basia@test.com')
        u1.set_password('tanie_maslo')
        self.assertFalse(u1.check_password('lalal'))
        self.assertTrue(u1.check_password('tanie_maslo'))



if __name__ == '__main__':
    unittest.main(verbosity=2)