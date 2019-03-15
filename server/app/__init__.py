from flask import Flask, render_template, request, Response
import os


app = Flask(__name__, template_folder='../../static', static_folder="../../static/dist")

from app import routes
