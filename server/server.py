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

@app.route('/parse', methods=['POST'])
def parse():
	toParse = request.values.get('html')
	print("result is " + toParse)
	res = html_parser.parseHTML(toParse)
	r = Response(res, status=200)
	return r

@app.route('/retrieve', methods=['POST'])
def retrieve():
	url = request.values.get('url')
	print(url)
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	toSend = req(url=url, headers=headers)
	try:
		html = urlopen(toSend).read()
		clean = html_parser.parseHTML(html)
		r = Response(clean, status=200)
	except Exception as e:
		print(e) 
		response = json.dumps("invalid url")
		r = Response(response, status=400)



@app.route('/first', methods=['POST'])
def findFirst():
	print(sys.version)
	url = request.values.get('url')
	name = request.values.get('name')
	# url = 'https://stratechery.com/feed'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	toSend = req(url=url, headers=headers)
	xml = urlopen(toSend).read()
	rss_feed = BeautifulSoup(xml, 'xml')
	links = rss_feed.find_all('guid')

	firstArticle = returnFirst(links)

	# html = firstArticle.html
	soup = specificArticle(name, firstArticle)
	soup = cleanTags(soup)
	soup = cleanAttributes(soup)

	open('output.html', 'w').close()
	text_file = open("output.html", "w")
	text_file.write(str(soup))
	text_file.close()

	r = Response(str(soup), status=200)
	return r

#find the first link that is not too short
def returnFirst(links):
	for link in links:
		url = link.string
		article = Article(url)

		article.download()
		article.parse()
		if (len(article.text) > 1000):
			# print(article.text)
			return article

def specificArticle(name, firstArticle):
	soup = BeautifulSoup(firstArticle.html, 'html.parser')

	open('nofilter.html', 'w').close()
	text_file = open("nofilter.html", "w")
	text_file.write(str(soup))
	text_file.close()

	if (name == 'stratechery'):
		return soup.find('article')
	elif (name == 'startupboy'):
		return soup.find('article')
	elif (name == 'Overcoming Bias'):
		return soup.find("div", id="content")
	# elif (name =='econlib'):
	# 	return soup.find("div", class_="article-single-page site-container post-container")
	else:
		return soup	

def cleanTags(soup):
	REMOVE_TAG = ['head', 'script', 'form', 'input']

	for tag in REMOVE_TAG:
		for e in soup.findAll(tag):
			e.extract()

	return soup

def cleanAttributes(soup):
	SAVE_ATTRIBUTES = ['href', 'src']
	SAVE_TAG = ['img']
	for tag in soup.recursiveChildGenerator():
		if tag.name not in SAVE_TAG:
			try:
				key_list = list( tag.attrs.keys() )
				for key in key_list:
					if key not in SAVE_ATTRIBUTES:
						del tag.attrs[key]
			except AttributeError: 
	        # 'NavigableString' object has no attribute 'attrs'
				pass
	return soup


@app.route('/poll', methods=['POST'])
def poll():
	print("polling");
	threading.Timer(5, poll).start()




