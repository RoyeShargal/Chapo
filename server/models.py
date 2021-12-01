# from api import db
import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

usersposts = db.Table('usersposts',
db.Column('user_id', db.Integer,db.ForeignKey('user.id')),
db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer)
    title = db.Column(db.String(100), index=True)
    content = db.Column(db.String(500), index=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    likes = db.Column(db.Integer)
    tags = db.Column(db.String(100))

    def __init__(self, title, userId, content,tags):
        self.title = title
        self.userid = userId
        self.content = content
        self.likes = 0
        self.tags=tags

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fullName = db.Column(db.String(50),index=True)
    email = db.Column(db.String(40), index=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    token = db.Column(db.String(100), unique=True)
    isActive = db.Column(db.Boolean)
    posts = db.relationship('Post', secondary=usersposts, backref=db.backref('postsliked', lazy = 'dynamic'))

    def __init__(self, fullName, email, password, token):
        self.fullName = fullName
        self.email = email
        self.password = password
        self.token = token

# class Comment(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     postid = db.Column(db.Integer)
#     content = db.Column(db.String(100))
#     userid = db.Column(db.Integer)
#
#     def __init__(self,postid,content,userid):
#         self.postid=postid
#         self.content=content
#         self.userid=userid
