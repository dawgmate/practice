from flask import Flask, url_for, render_template, redirect, request
from markupsafe import escape

app=Flask(__name__)

app.secret_key="dsnsdalsd"

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
        
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    if 

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == "__main__":
    app.run(debug = True)