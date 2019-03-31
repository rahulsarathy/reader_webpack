from flask import Flask, render_template, request, Response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__, template_folder='../../static/templates', static_folder="../../static/dist")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors