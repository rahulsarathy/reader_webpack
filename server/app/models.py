from app import app, db, JSON, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    kindle_email = db.Column(db.String(120), index=True, unique=True)
    subscribed = db.relationship('Blogs', backref='owner')

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password)

    def check_password(self, password):
    	return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {} with id {}>'.format(self.username, self.id)

class Blogs(db.Model):
	stratechery = db.Column(db.Boolean, unique=False, default=False)
	startupboy = db.Column(db.Boolean, unique=False, default=False)
	bryan_caplan_econlib = db.Column(db.Boolean, unique=False, default=False)
	marginal_revolution = db.Column(db.Boolean, unique=False, default=False)
	ribbonfarm = db.Column(db.Boolean, unique=False, default=False)
	melting_asphalt = db.Column(db.Boolean, unique=False, default=False)
	overcoming_bias = db.Column(db.Boolean, unique=False, default=False)
	elaine_ou = db.Column(db.Boolean, unique=False, default=False)
	eugene_wei =db.Column(db.Boolean, unique=False, default=False)
	meaningness = db.Column(db.Boolean, unique=False, default=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)



@login.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': Users}