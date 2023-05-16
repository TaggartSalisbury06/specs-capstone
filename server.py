from flask import Flask, render_template, redirect, request
from model import connect_to_db
app = Flask(__name__)

# Home route
@app.route("/")
def home():
  return render_template("home.html")

if __name__ == "__main__":
  connect_to_db(app)
  app.run(host="localhost", port=8000, debug=True)