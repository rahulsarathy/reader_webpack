from app import app, db, JSON
from werkzeug.security import generate_password_hash, check_password_hash

data = {
	'stratechery': False,
	'startupboy': False,
	'bryan_caplan_econlib': False,
	'marginal_revolution': False,
	'ribbonfarm': False,
'melting_asphalt': False,
	'overcoming_bias': False,
	'elaine_ou': False,
	'eugene_wei': False,
	'meaningness': False
}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    kindle_email = db.Column(db.String(120), index=True, unique=True)
    blogs = db.Column(JSON, default=lambda: data )

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password)

    def check_password(self, password):
    	return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)   

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': Users}