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
import pickle

data = [
	{
		'name': "stratechery",
		'url': "https://stratechery.com/feed",
	},
	{
		'name': "startupboy",
		'url': "https://startupboy.com/feed",
	},
	{
		'name': "Bryan Caplan Econlib",
		'url': "https://www.econlib.org/feed/indexCaplan_xml",
	},
	{
		'name': "Marginal Revolution",
		'url': "https://feeds.feedburner.com/marginalrevolution/"
	},
	{
		'name': "Ribbon Farm",
		'url': "https://ribbonfarm.com/feed",
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

	book_creator.createEBook(name)

	r = Response(str(soup), status=200)
	return r

@app.route('/poll', methods=['POST'])
def poll():

	for blog in data:
		name = data['name']
		url = data['url']

		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
		toSend = req(url=url, headers=headers)

		xml = urlopen(toSend).read()
		rss_feed = BeautifulSoup(xml, 'xml')

		new_update = rss_feed.find('lastBuildDate')
		if new_update is not None:
			new_update = time.strptime(rss_feed.find('lastBuildDate').text, "%a, %d %b %Y %H:%M:%S +0000")
		else:
			new_update = time.strptime("Mon, 11 Mar 2019 17:45:34 +0000", "%a, %d %b %Y %H:%M:%S +0000")

		file = open('last.txt', 'rb')
		time_table = pickle.load(file)
		file.close()

		if name in time_table:
			last_updated = time.strptime(time_table[name], "%a, %d %b %Y %H:%M:%S +0000")

		# if no new update do nothing
		if last_updated == new_update:
			continue

		time_table[name] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", new_update)
		file = open('last.txt', 'wb')
		pickle.dump(time_table, file)
		file.close()

		book_creator.createEBook(name)




	threading.Timer(3600, poll).start()




