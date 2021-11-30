import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import models
from models import *
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import pytest
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_session import Session

class TestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object('config')
        app.config['TESTING'] = True

        bcrypt = Bcrypt(app)
        CORS(app, supports_credentials=True)
        server_session = Session(app)
        # app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        db.init_app(app) #Add this line Before migrate line
        migrate = Migrate(app, db)
        with app.app_context():
            db.create_all()

        self.app = app.test_client()
        self.user = User('Roye','roye@gmail.com','roy.com','justapassword')
        self.p = models.Post.query.all()
        pass

    def test_allPosts(self):
        print(self.p)
        pass

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)
#
#     def test_new_user(self):
#         allUsers=User.query.all()

#         numOfallUsers=len(allUsers)
#         db.session.add(self.user)
#         allUsersNEW=User.query.all()
#         numOfallUsersNEW=len(allUsersNEW)
#         self.assertEqual(self.user.email, 'roye.shargal@gmail.com')


#     def test_new_user_with_fixture(test_new_user):
#         """
#         GIVEN a User model
#         WHEN a new User is created
#         THEN check the email, hashed_password,
#         """
#         assert new_user.email == 'roye.shargal@gmail.com'
#         assert new_user.hashed_password != 'justapassword'

    def tearDown(self):
        db.session.remove()
#         db.drop_all()

if __name__ == '__main__':
    unittest.main()