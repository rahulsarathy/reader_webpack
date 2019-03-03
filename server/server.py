from flask import Flask
from flask import render_template

app = Flask(__name__, template_folder='../static', static_folder="../static/dist")

@app.route('/')
def hello_world(name=None):
    return render_template('index.html', name=name)
