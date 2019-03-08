from flask import Flask
import html_parser
import json
from urllib.request import urlopen
from urllib.request import Request as req
from flask import render_template, request, Response
import time, threading, webbrowser, random
from newspaper import Article
from bs4 import BeautifulSoup


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
	url = request.values.get('url')
	print("finding " + url)
	# url = 'https://stratechery.com/feed'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	toSend = req(url=url, headers=headers)
	xml = urlopen(toSend).read()
	soup = BeautifulSoup(xml, 'xml')
	links = soup.find_all('guid')
	# print(links)
	firstArticle = returnFirst(links)
	html = firstArticle.html
	open('output.html', 'w').close()
	text_file = open("output.html", "w")
	text_file.write(html)
	text_file.close()

	r = Response(html, status=200)
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

@app.route('/poll', methods=['POST'])
def poll():
	print("polling");
	threading.Timer(5, poll).start()




