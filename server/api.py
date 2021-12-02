from flask import Flask, jsonify, request, session,redirect, abort, Response, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
# from flask.helpers import send_from_directory
from flask_bcrypt import Bcrypt
from flask_session import Session
from config import ApplicationConfig
from werkzeug.utils import secure_filename
import json
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
import os
import pathlib
import models
from models import *
from flask_migrate import Migrate
import requests
import uuid #responsible for the unique token for each user.
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app = Flask(__name__)
#, static_folder="../client/build", static_url_path=''
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)

db.init_app(app) #Add this line Before migrate line
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()
#
# @app.route('/home')
# def serve():
#     print('ey')
#     return send_from_directory(app.static_folder, 'index.html')

GOOGLE_CLIENT_ID = "207357768932-cfip3jmo203p7s6q76bhggoldvmsrm05.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent,"client_secret.json")
flow = Flow.from_client_secrets_file(client_secrets_file = client_secrets_file,
scopes = ["https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email","openid"],
redirect_uri = "http://127.0.0.1:5000/callback")


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

@app.route("/logingoogle")
def loginGoogle():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


def login_is_required(function):
    def wrapper():
        if "google_id" not in session:
            return abort(401) #auth required
        else:
            return function()
    return wrapper

@app.route("/protected_area")
@login_is_required
def protected_area():
    return 'protected'

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500) # STATE DOES NOT MATCH

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
    id_token = credentials._id_token,
    request=token_request,
    audience = GOOGLE_CLIENT_ID)
    return id_info

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
    app.debug=True
    app.run()
