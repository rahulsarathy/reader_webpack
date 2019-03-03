from flask import Flask
from flask import render_template, request, Response
import html_parser
import json

app = Flask(__name__, template_folder='../static', static_folder="../static/dist")

@app.route('/')
def hello_world(name=None):
    return render_template('index.html', name=name)

@app.route('/parse', methods=['POST'])
def parse():
	print(request.values)
	res = json.dumps("hi")
	r = Response(res, status=200)
	return r
