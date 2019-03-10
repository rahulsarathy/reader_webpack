from flask import Flask
import html_parser
import json
from urllib.request import urlopen
from urllib.request import Request as req
from flask import render_template, request, Response
import time, threading, webbrowser, random
from newspaper import Article
from bs4 import BeautifulSoup
import sys
import cleaning
import book_creator

data = [
	{
		'name': "stratechery",
		'url': "https://stratechery.com/feed",
		'selector': "content"
	},
	{
		'name': "startupboy",
		'url': "https://startupboy.com/feed",
		'selector': "content"
	},
	{
		'name': "Bryan Caplan Econlib",
		'url': "https://www.econlib.org/feed/indexCaplan_xml",
		'selector': "post-content"
	},
	{
		'name': "Marginal Revolution",
		'url': "https://feeds.feedburner.com/marginalrevolution/"
	},
	{
		'name': "Ribbon Farm",
		'url': "https://ribbonfarm.com/feed",
		'selector': "content"
	},
	{
		'name': "Melting Asphalt",
		'url': "https://meltingasphalt.com/feed/"

	},
	{
		'name': "Overcoming Bias",
		'url': "http://www.overcomingbias.com/feed"
	}
];


app = Flask(__name__, template_folder='../static', static_folder="../static/dist")

@app.route('/')
def main(name=None):
    return render_template('index.html', name=name)

@app.route('/first', methods=['POST'])
def retrieveHTML():
	url = request.values.get('url')
	name = request.values.get('name')
	soup = cleaning.findFirst(url, name)

	book_creator.createEBook()

	r = Response(str(soup), status=200)
	return r

@app.route('/poll', methods=['POST'])
def poll():
	print("polling");
	threading.Timer(5, poll).start()




