from app import db, login
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import json
import enum
from sqlalchemy import Enum
import time
import jwt

blogs = {
    'stratechery': {
        'display': "Stratechery",
        'url': "https://stratechery.com/feed",
        'category': ['technology'],
        'color': "#FCA71F",
        'page': 'https://stratechery.com/',
        'image': True

    },
    'startupboy':
    {
        'display': "Startupboy",
        'url': "https://startupboy.com/feed",
        'category': ['technology'],
        'color': "#D7A174",
        'page': 'https://startupboy.com/',
        'image': True


    },
    'bryan_caplan_econlib':
    {
        'display': 'Bryan Caplan\'s Econlib',
        'url': "https://www.econlib.org/feed/indexCaplan_xml",
        'category': ['economics'],
        'color': "#0d1226",
        'page': 'https://www.econlib.org/author/bcaplan/',
        'image': True


    },
    'marginal_revolution':
    {       
        'display': "Marginal Revolution",
        'url': "https://feeds.feedburner.com/marginalrevolution/",
        'category': ['economics'],
        'color': "#00B88E",
        'page': 'https://marginalrevolution.com/',
        'image': True

    },
    'ribbonfarm':
    {
        'display': "Ribbon Farm",
        'url': "https://ribbonfarm.com/feed",
        'custom_parse': True,
        'category': ['rationality'],
        'color': "#30162b",
        'page': 'https://www.ribbonfarm.com/',
        'image': True


    },
    'melting_asphalt':
    {
        'display': "Melting Asphalt",
        'url': "https://feeds.feedburner.com/MeltingAsphalt",
        'category': ['rationality'],
        'color': "#970004",
        'page': 'https://meltingasphalt.com/',
        'image': True

    },
    'overcoming_bias':
    {
        'display': 'Overcoming Bias',
        'url': "http://www.overcomingbias.com/feed",
        'category': ['rationality', 'economics'],
        'color': "#000080",
        'page': 'www.overcomingbias.com',
        'image': False
    },
    # 'elaine_ou':
    # {
    #     'display': 'Elaine Ou',
    #     'url': 'https://elaineou.com/feed/',
    #     'category': ['personal_musings'],
    #     'color': "#4286f4"
    # },
    # 'eugene_wei':
    # {
    #     'display': 'Eugene Wei',
    #     'url': 'https://eugene-wei.squarespace.com/blog?format=rss',
    #     'category': ['personal_musings'],
    #     'color': "#4286f4"
    # },
    # 'cato': {
    #     'display': 'Cato Institute',
    #     'url': 'https://www.cato.org/rss/recent-opeds',
    #     'category': ['think_tanks'],
    #     'custom_parse': True
    # },
    # 'aei': {
    #     'display': 'American Enterprise Institute',
    #     'url': 'https://http://www.aei.org/feed/',
    #     'category': ['think_tanks'],
    #     'custom_parse': True
    # },
    # 'brookings': {
    #     'display': 'Brookings Institution',
    #     'url': 'http://feeds.feedblitz.com/BrookingsRSS/programs/economics',
    #     'category': ['think_tanks', 'economics'],
    #     'custom_parse': True
    # },
    'niskanen': {
            'display': 'Niskanen Center',
            'url': 'https://niskanencenter.org/feed/',
            'category': ['think_tanks', 'economics'],
            'color': "#19525F",
            'page': 'https://niskanencenter.org/',
            'image': False
    },
    'mercatus': {
        'display': 'Mercatus Center',
        'url': 'https://www.mercatus.org/feed',
        'category': ['think_tanks', 'economics'],
        'custom_parse': True,
        'color': "#323946",
        'page': 'https://www.mercatus.org/',
        'image': True
    }, 
    # 'pew': {
    #     'display': 'Pew Research Center',
    #     'url': 'http://www.pewresearch.org/feed/',
    #     'category': ['think_tanks']
    # }
}

default_time = time.strptime("Mon, 11 Mar 2019 17:45:34 +0000", "%a, %d %b %Y %H:%M:%S +0000")

class BlogName(enum.Enum):
	stratechery = 1
	startupboy = 2
	bryan_caplan_econlib = 3
	marginal_revolution = 4
	ribbonfarm = 5
	melting_asphalt = 6
	overcoming_bias = 7
	elaine_ou = 8
	eugene_wei = 9
	meaningness = 10
	cato = 11
	aei = 12
	brookings = 13
	niskanen = 14
	mercatus = 15
	pew = 16

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    kindle_email = db.Column(db.String(120), index=True, unique=True)
    blogs = db.relationship('Blog', backref='owner')

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password)

    def check_password(self, password):
    	return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {} with id {}>'.format(self.username, self.id)

class Blog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	name = db.Column(Enum(BlogName))

	def __repr__(self):
		return '<User {} wants emails from {}>'.format(self.user_id, self.name)
	
class Poll(db.Model):
    name = db.Column(Enum(BlogName), primary_key=True)
    time = db.Column(db.DateTime, default=default_time)

    def __repr__(self):
        return '<Polled {} at {}>'.format(self.name, self.time)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))
