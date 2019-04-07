import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, render_template, request, Response, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()

def create_app(config_class=Config):
	app = Flask(__name__, template_folder='../static/templates', static_folder="../static/dist")

	app.config.from_object(config_class)
	#app.config.update(mail_settings)

	db.init_app(app)
	migrate.init_app(app, db)
	login.init_app(app)
	mail.init_app(app)

	from app.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	from app.auth import bp as auth_bp
	app.register_blueprint(auth_bp, url_prefix='/auth')

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	return app

from app import models
from app.models import Poll, BlogName
