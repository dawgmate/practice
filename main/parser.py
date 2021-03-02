from flask import Flask, render_template
from bs4 import BeautifulSoup
from csv import writer
from pymongo import MongoClient
from pprint import pprint
import re
import requests
from Container import ContentBox
from lxml import html

client = MongoClient("mongodb://localhost:27017/")
db=client["RomeDb"]


def parse(content, container):
    str1=content.replace(":", ",").replace(";", ",").replace(".", ",").replace("\"",",").replace("–",",").replace(",", " ")
    tmp = str1.split(" ")
    for item in tmp:
        if item not in container:
            container[item] = 1
        else: 
            container[item] = container.get(item) + 1
    return container

source = requests.get('https://www.pravda.com.ua/news/')

soup = BeautifulSoup(source.content, 'html.parser')
soup.em.decompose()
posts = soup.findAll(class_='article_news_list')
dictionary = {}
mywords = db["Words"]
myposts = db["Posts"]
with open('articles.csv','w', encoding='cp1251') as csv_file:
    csv_writer = writer(csv_file)
    headers=['Title', 'Link', 'Time']
    csv_writer.writerow(headers)
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
        csv_writer.writerow([title, link, date])
    for words in dictionary:
        word={
            'word' : words,
            'number' : dictionary.get(words)
        }
        pprint(words)
        x= mywords.insert_one(word)
