import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	ADMINS = [os.environ['MAIL_USER']]
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USERNAME = os.environ.get('MAIL_USER')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
	URL = os.environ.get('HOME_URL') or 'http://127.0.0.1:5000/'
	#MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')