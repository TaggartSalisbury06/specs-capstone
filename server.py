from flask import Flask, render_template, redirect, request, session, flash
from model import connect_to_db, db, User, Post, Message
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from flask_bcrypt import check_password_hash
import crud

app = Flask(__name__)
login_manager = LoginManager()

app.secret_key = "dev"

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# Home route
@app.route("/")
def index():  
  posts = Post.query.all()
  if current_user.is_authenticated:
    username = current_user.username
    flash(f"Logged in as {username}")
  else:
    username = "Guest"

  return render_template("home.html", username=username, posts=posts)

# Users route
@app.route("/users")
def users():
  posts = Post.query.all()
  users = User.query.all()
  return render_template("users.html", users=users, posts=posts)

# Login route
@app.route("/posts/create", methods=["POST"])
def create_post():
  post_content = request.form["post_content"]
  user = current_user

  new_post = Post(post_content=post_content, user_id=user.id)
  db.session.add(new_post)
  db.session.commit()

  return redirect("/posts")

@app.route("/messages")
@login_required
def messages():
  messages = Message.query.filter((Message.sender_id == current_user.id) | (Message.recipient_id == current_user.id)).all()
  return render_template("messages.html", messages=messages)


@app.route("/message/create", methods=["GET", "POST"])
@login_required
def create_message():
  if request.method == "GET":
    users = User.query.all()
    return render_template("create_message.html", users=users)

  recipient_id = request.form["recipient_id"]
  message_content = request.form["message_content"]

  recipient = User.query.get(recipient_id)
  if recipient is None:
    flash("Invalid recipient. Please select a valid user.")
    return redirect("/create-message")

  new_message = Message(message_content=message_content, sender=current_user, recipient=recipient)
  db.session.add(new_message)
  db.session.commit()

  flash("Message sent successfully!")
  return redirect("/messages")

@app.route("/login", methods=["POST"])
def login():
  username = request.form["username"]
  password = request.form["password"]

  user = User.query.filter_by(username=username).first()

  if user is None:
    return render_template("login.html", error="Invalid username or password")

  login_user(user)

  return redirect("/")

@app.route("/profile")
def profile():
  if current_user.is_authenticated:
    return render_template("profile.html", current_user=current_user)
  else:
    return redirect("/login")  # Redirect to the login page if the user is not authenticated

@app.route("/posts")
def display_posts():
  posts = Post.query.all()
  return render_template("posts.html", posts=posts)

@app.route("/users/create", methods=["GET", "POST"])
def create_user():
  if request.method == "GET":
    return render_template("create_user.html")

  username = request.form["username"]
  email = request.form["email"]
  password = request.form["password"]

  user = User(username=username, email=email, password=password)
  db.session.add(user)
  db.session.commit()

  return redirect("/")

@app.route("/logout")
def logout():
  logout_user()
  return redirect("/")

if __name__ == "__main__":
  connect_to_db(app)
  app.run(host="localhost", port=8000, debug=True)
