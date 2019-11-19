from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    submittedPosts = db.relationship('Post', backref='author', lazy='dynamic')
    savedPosts = db.relationship('Post', backref='saved', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    description = db.Column(db.String(512), index=True)
    timeStamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.title)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Long = db.Column(db.Float, index=True)
    Lat = db.Column(db.Float, index=True)

    post = db.relationship('Post', backref='location', lazy='dynamic')

    def __repr__(self):
        return '<location {}>'.format(self.post)



