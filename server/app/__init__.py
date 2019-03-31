from flask import Flask, render_template, request, Response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import os

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

app = Flask(__name__, template_folder='../../static/templates', static_folder="../../static/dist")
app.config.from_object(Config)
app.config.update(mail_settings)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

from app import routes, models, errors