from model import db, User, Post, Message
# from server import app
# User CRUD operations

def create_user(username, password, email, bio, avatar_path):
  user = User(username=username, password=password, email=email, bio=bio, avatar_path=avatar_path)
  db.session.add(user)
  db.session.commit()
  return user

def get_user_by_id(user_id):
  return User.query.get(user_id)

def get_user_by_username(username):
  return User.query.filter_by(username=username).first()

def get_all_users():
    return User.query.all()

def update_user(user_id, username=None, password=None, email=None, bio=None, avatar_path=None):
  user = get_user_by_id(user_id)
  if user:
    if username:
      user.username = username
    if password:
      user.password = password
    if email:
      user.email = email
    if bio:
      user.bio = bio
    if avatar_path:
      user.avatar_path = avatar_path
      db.session.commit()
      return user
    return None

def delete_user(user_id):
  user = get_user_by_id(user_id)
  if user:
    db.session.delete(user)
    db.session.commit()
    return True
  return False

# Post CRUD operations

def create_post(content, user_id):
  post = Post(content=content, user_id=user_id)
  db.session.add(post)
  db.session.commit()
  return post

def get_post_by_id(post_id):
  return Post.query.get(post_id)

def get_all_posts():
  return Post.query.all()

def update_post(post_id, content):
  post = get_post_by_id(post_id)
  if post:
    post.content = content
    db.session.commit()
    return post
  return None

def delete_post(post_id):
  post = get_post_by_id(post_id)
  if post:
    db.session.delete(post)
    db.session.commit()
    return True
  return False

# Message CRUD operations

def create_message(content, sender_id, recipient_id):
  message = Message(content=content, sender_id=sender_id, recipient_id=recipient_id)
  db.session.add(message)
  db.session.commit()
  return message

def get_message_by_id(message_id):
  return Message.query.get(message_id)

def get_all_messages():
  return Message.query.all()

def update_message(message_id, content):
  message = get_message_by_id(message_id)
  if message:
    message.content = content
    db.session.commit()
    return message
  return None

def delete_message(message_id):
  message = get_message_by_id(message_id)
  if message:
    db.session.delete(message)
    db.session.commit()
    return True
  return False
