from flask import Flask, url_for, render_template, redirect, request
from bs4 import BeautifulSoup
from csv import writer
import re
import requests
from markupsafe import escape


app=Flask(__name__)

app.secret_key="knu162020"

@app.route("/")
@app.route("/home")
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
    return 

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == "__main__":
    app.run(debug = True)