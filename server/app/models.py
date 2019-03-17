from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    kindle_email = db.Column(db.String(120), index=True, unique=True)
    stratechery = db.Column(db.Boolean, index=True, default=False)
    startupboy = db.Column(db.Boolean, index=True, default=False)


    def __repr__(self):
        return '<User {}>'.format(self.username)   