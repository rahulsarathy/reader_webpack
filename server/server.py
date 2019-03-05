from flask import Flask
import html_parser
import json
from urllib.request import urlopen
from urllib.request import Request as req
from flask import render_template, request, Response


app = Flask(__name__, template_folder='../static', static_folder="../static/dist")

@app.route('/')
def hello_world(name=None):
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
	return r

