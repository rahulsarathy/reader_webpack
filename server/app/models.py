from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import json
import enum
from sqlalchemy import Enum
from time import time
import jwt

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
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
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
	
@login.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': Users}