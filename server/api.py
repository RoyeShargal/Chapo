from flask import Flask, jsonify, request, session, abort, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_session import Session
from config import ApplicationConfig
from werkzeug.utils import secure_filename
import json
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
import os
import models
from models import *
from flask_migrate import Migrate
import uuid #responsible for the unique token for each user.

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)

db.init_app(app) #Add this line Before migrate line
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

def postSerializer(post):
    user = User.query.filter_by(id=post.userid).first()

    return{
    'id': post.id,
    'title': post.title,
    'content': post.content,
    'authorId': post.userid,
    'authorName': user.fullName,
    'date': post.date,
    'likes':post.likes,
      'tags': post.tags}

def commentSerializer(comment):
    user = User.query.filter_by(id=comment.userid).first()
    return{
    'id': comment.id,
    'content': comment.content,
    'authorId': comment.userid,
    'authorName': user.fullName,
    }

def userSerializer(user):
    return{
    'id': user.id,
    'fullName': user.fullName,
    'email': user.email,
    'date': user.date,
    'token': user.token,
    'isActive':user.isActive}

def relationSerializer(usersposts):
    return{
    'user_id':likedposts.user_id,
    'post_id': likedpsots.post_id
    }

@app.route("/postsbytags", methods=["GET","POST"], strict_slashes=False)
def getPostsByTags():
    tags = request.json['tags']
    # get the posts that has the specific tag:
    search = "%{}%".format(tags)
    posts = Post.query.filter(Post.tags.like(search)).all()
    print(posts)
    return jsonify([*map(postSerializer, posts)])

@app.route("/users", methods=["GET"], strict_slashes=False)
def users():
    users = User.query.all()
    return jsonify([*map(userSerializer, users)])

@app.route("/posts", methods=['GET'], strict_slashes=False)
def allPosts():
    posts = Post.query.all()
    return (jsonify([*map(postSerializer, posts)]))

# @app.route("/specificposts", methods=['POST', 'GET'], strict_slashes=False)
# def specificPosts():
#     reqTable = usersposts.query.all()


#     requiredPosts = []
#     userid = session.get("user_id")
#     user = User.query.filter_by(id=1).first()
#     post = Post.query.all()
#     for x in post:
#         print(x.postsliked)
#
#     return (jsonify([*map(postSerializer, requiredPosts)]))


@app.route("/deletepost", methods=['GET','POST'])
def deletePost():
    print('reached')
    postToDeleteId = request.json['postId']
    print("POST TO DELETE", postToDeleteId)
    post = Post.query.filter_by(id=postToDeleteId).first()
    db.session.delete(post)
    db.session.commit()

@app.route("/likeapost", methods=['GET', 'POST'])
def likePost():
    post_id = request.json['postId']
    user_id = session.get("user_id")

    post = Post.query.filter_by(id=post_id).first()
    user = User.query.filter_by(id=user_id).first()
    if user == None:
        jsonify({"Error": "User Does Not Exists."}), 401
    if user in post.postsliked:
        print('error mate')
    else:
        post.postsliked.append(user)
        db.session.commit()
        print('alright')
    return 'Liked!'

@app.route("/specificposts", methods=['POST', 'GET'], strict_slashes=False)
def specificPosts():
    posts = Post.query.all()
    userid = session.get("user_id")
    user = User.query.filter_by(id=userid).first()
    requiredPosts = []
    for post in posts:
        if user in post.postsliked:
            requiredPosts.append(post)
    return (jsonify([*map(postSerializer, requiredPosts)]))


# @app.route("/comments", methods=['GET','POST'], strict_slashes=False)
# def SpecificPostComments():
#     identification = request.json['postID']
#     print(identification)
#     comments = Comment.query.filter_by(postid=identification)
#     return (jsonify([*map(commentSerializer, comments)]))

# @app.route("/allcomments", methods=['GET'],strict_slashes=False)
# def allComments():
#     allComments = Comment.query.all()
#     return (jsonify([*map(commentSerializer, allComments)]))
#
# #NEWCOMMENT
# @app.route("/newcomment", methods=['POST'],strict_slashes=False)
# def newcomment():
#     post_id = request.json['postid']
#     content=request.json['content']
#     user_id = request.json['userid']
#
#     newComment = Comment(postid=post_id,content=content,userid=user_id)
#     db.session.add(newComment)
#     db.session.commit()
#     return('added comment')

#NEWPOST
@app.route("/newpost", methods=['POST'], strict_slashes=False)
def newPost():
    user_id = request.json['userid']
    print("user id is:", user_id)
    title = request.json['title']
    tags = request.json['tags']
    content = request.json['content']
    print("title is:", title)
    user = User.query.filter_by(id=user_id).first()
    if user.isActive == True:
        newPost = Post(title = title, userId=(user_id), content=content, tags=tags)
        db.session.add(newPost)
        db.session.commit()
    else:
        return ('Well, you are logged off technically.')
    return ('added post')

@app.route("/signup", methods=["POST"], strict_slashes=False)
def SignUpNow():
    fullName = request.json['fullName']
    email = request.json['email']
    password = request.json['password']
    secret_token = str(uuid.uuid4())
    user_exists = User.query.filter_by(email=email).first() is not None
    if user_exists:
        return jsonify({"error": "User already exists"}), 409
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    newUser = User(fullName = fullName, email=email, password=hashed_password,token=secret_token)
    db.session.add(newUser)
    newUser.isActive=False
    db.session.commit()
    return ('ADDED USER')


@app.route("/login", methods=['POST'])
def login_user():
    email = request.json['email']
    new_email = email.lower()
    password = request.json['password']
    user = User.query.filter_by(email=new_email).first()

    if user is None:
        return jsonify({"Error": "User Does Not Exists."}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"Error": "Wrong Password."}), 401


    session["user_id"] = user.id
    user.isActive = True
    db.session.commit()

    print("user id ", session["user_id"])

    return jsonify({
        "email": user.email,
        "id": user.id
        })

@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"Error": "User Does Not Exists."}), 401
    else:
        print(user_id)
        user = User.query.filter_by(id=user_id).first()
    return jsonify({
            "email": user.email,
            "fullName": user.fullName,
            "id": user.id,
            "token": user.token,
            "date": user.date
            })



@app.route("/logout", methods=["POST"])
def logout_user():
    user = User.query.filter_by(id=session.get("user_id")).first()
    user.isActive = False
    db.session.commit()
    session.pop("user_id")

    return "200"

@app.route("/changepassword", methods=['POST'])
def change_pass():
    user_id = request.json['userid']
    print("USER ID IS", user_id)
    password = request.json['password']
    user = User.query.filter_by(id=user_id).first()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user.password = hashed_password
    print(password)
    db.session.merge(user)

    db.session.commit()
    return "Success!"

if __name__=="__main__":
    app.run(debug=True)
