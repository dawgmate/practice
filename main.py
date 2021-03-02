from flask import Flask, url_for, render_template, redirect, request, session , flash
from datetime import timedelta
from bs4 import BeautifulSoup
from lxml import html
from pprint import pprint
import re
import requests
from pymongo import MongoClient, DESCENDING

from markupsafe import escape


app=Flask(__name__)

app.secret_key="knu162020"
app.permanent_session_lifetime = timedelta(hours = 12)
client = MongoClient("mongodb://localhost:27017/")
db=client["RomeDb"]
myUsers = db["Users"]
site=""

mywords = db["Words"]
myposts = db["Posts"]

def parse(content, container):
    str1=content.replace(":", ",").replace(";", ",").replace(".", ",").replace("\"",",").replace("–",",").replace("-",",").replace(" ",",").replace(",", " ").strip()
    tmp = str1.split(" ")
    for item in tmp:
        if len(item)>5:
            if item not in container:
                container[item] = 1
            else: 
                container[item] = container.get(item) + 1
    return container


@app.route("/")
@app.route("/home")
def index():
    if "user" in session:
        return redirect(url_for("mainpage"))
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        password = request.form["pw"]
        if not myUsers.find_one({'username': user, 'password': password}):
            flash("Wrong username or password!","info")
            return render_template("login.html")
        session["user"]= user
        return redirect(url_for("user")) 
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user")
    flash("You successfuly logged out", "info")
    return redirect(url_for("login"))

@app.route("/user")
def user():
    if "user" in session:
        user=session["user"]
        return render_template("user.html", Username=user)
    else:
        flash("You're not logged in!", "info")
        return redirect(url_for("login"))

@app.route("/register", methods = ["POST", "GET"])
def register():
    if "user" in session:
        return redirect(url_for("user"))
    users = myUsers["username"]
    for _ in myUsers.find({'field':'value'}):
                pprint(_)
    passwords = myUsers["password"]

    if request.method == "POST":
        user = request.form["nm"]
        password = request.form["pw"]
        cpassword = request.form["cpw"]
        if users.count() != 0:
            if users.find_one({'username' : user}):
                flash("This username is taken", "info")
                return redirect(url_for("/register"))
        else:
            if password == cpassword:
                _user = {
                    'username': user,
                    'password': password
                }
                x = myUsers.insert_one(_user)
                session["user"]=user
                flash("You've successfuly signed up!")
                return redirect(url_for("user"))
            else:
                flash("Wrong password", "info")
                return render_template("register.html")
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("register.html")

@app.route("/main", methods = ["POST", "GET"]) 
def mainpage():
    global site
    if request.method == "POST":
        site = request.form["sel"]
        print(site)
        return redirect(url_for("work"))
    return render_template("main.html")

@app.route("/work", methods= ["POST", "GET"])                 
def work():
    global mywords, myposts
    dictionary = {}
    if "Words" not in db.list_collection_names():
        mywords = db["Words"]
    if "Posts" not in db.list_collection_names():
        myposts["Posts"]
    global site
    if site == "https://www.pravda.com.ua/news/":
        source = requests.get(site)
        soup = BeautifulSoup(source.content, 'html.parser')
        em_tag=soup.em
        em_tag.decompose()             #WTF???
        posts = soup.findAll(class_='article_news_list')
        for post in posts:
            title = post.find(class_='article_content').get_text().replace('\n',' ')
            link = post.find('a')['href']
            date = post.find(class_='article_time').get_text()
            _post = {
                'title' : title,
                'link' : link,
                'date' : date
            }
            x= myposts.insert_one(_post)
            title = title.lower()
            dictionary=parse(title, dictionary)
    # elif site == "https://socportal.info/":
    #     source = requests.get(site)
    #     soup = BeautifulSoup(source.content, 'html.parser')
    #     posts = soup.findAll(class_="news-feed__item")
    #     for post in posts:
    #         title = post.find(class_='news-feed__item-link').get_text().replace('\n',' ')
    #         link = post.find(class_='news-feed__item-link')['href']
    #         date = post.find(class_='news-feed__item-time').get_text()
    #         _post = {
    #             'title' : title,
    #             'link' : link,
    #             'date' : date
    #         }
    #         x= myposts.insert_one(_post)
    #         title = title.lower()
    #         dictionary=parse(title, dictionary)
    for words in dictionary:
        word={
            'word' : words,
            'number' : dictionary.get(words)
        }
        x= mywords.insert_one(word)
    if request.method=="POST":
        mywords.drop()
        myposts.drop()
        return redirect(url_for("mainpage"))
    return render_template("work.html", site= site, words= sorted(dictionary.items(), key=lambda x: x[1], reverse=True), posts = myposts)


if __name__ == "__main__":
    app.run(debug = True) 