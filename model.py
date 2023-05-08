import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  username = db.Column(db.String, nullable = False)
  password = db.Column(db.String, unique = True, nullable = False)

class Post(db.Model):

  __tablename__ = "posts"

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  post_content = db.Column(db.String, nullable = False)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
  post_date = db.Column(db.datetime)

class Comment(db.Model):

  __tablename__ = "comments"

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  comment_content = db.Column(db.String, nullable = False)
  comment_date = db.Column(db.datetime)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
  post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable = False)

class Mesage(db.Model):

  __tablename__ = "messages"

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  content = db.Column(db.String, nullable = False)
  sent_time = db.Column(db.datetime)
  sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
  recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)