import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  username = db.Column(db.String, nullable = False)
  password = db.Column(db.String, unique = True, nullable = False)
  bio = db.Column(db.String, nullable = True)
  email = db.Column(db.String, unique = True, nullable = False)
  avatar_path = db.Column(db.String)

  posts = db.relationship('Post', backref='user', lazy=True)

  def check_password(self, password):
    """
    Checks if the given password matches the password for this user.

    Args:
      password: The password to check.

    Returns:
      True if the password matches, False otherwise.
    """

    # Get the hashed password from the database.
    hashed_password = self.password

    # Check if the given password matches the hashed password.
    return check_password_hash(hashed_password, password)

  def is_active(self):
    # Customize the logic to determine whether the user is active or not
    return True  # Replace with your logic

  def get_id(self):
    return str(self.id)
  
  def is_authenticated(self):
    return True

  def __repr__(self):
    return f"<User id={self.id} username={self.username} email={self.email}>"

class Post(db.Model):
  __tablename__ = "posts"

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  post_content = db.Column(db.String, nullable = False)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
  post_date = db.Column(db.DateTime)

  def __repr__(self):
    return f"<Post id={self.id} post_content={self.post_content} post_date={self.post_date}>"

class Comment(db.Model):
  __tablename__ = "comments"

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  comment_content = db.Column(db.String, nullable = False)
  comment_date = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
  post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable = False)

  def __repr__(self):
    return f"<Comment id={self.id} comment_content={self.comment_content} comment_date={self.comment_date}>"

class Message(db.Model):
  __tablename__ = "messages"

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  content = db.Column(db.String, nullable = False)
  sent_time = db.Column(db.DateTime)
  sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
  recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

  def __repr__(self):
    return f"<Message id={self.id} content={self.content} sent_time={self.sent_time}>"


def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo=False):
  flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
  flask_app.config["SQLALCHEMY_ECHO"] = echo
  flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

  db.app = flask_app
  db.init_app(flask_app)

  print("Connected to the db!")


if __name__ == "__main__":
  from server import app

  connect_to_db(app)

