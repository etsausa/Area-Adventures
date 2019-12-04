from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('Post', backref='author', lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Long = db.Column(db.Float, index=True)
    Lat = db.Column(db.Float, index=True)

    street = db.Column(db.String)

    post = db.relationship('Post', backref='location', lazy='dynamic')

    def __repr__(self):
        return '<location {}>'.format(self.post)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    description = db.Column(db.String(512), index=True)
    timeStamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_submitted = db.Column(db.Boolean)
    user_id =  db.Column(db.Integer, db.ForeignKey(User.id))
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id))

    def __repr__(self):
        return '<Post {}>'.format(self.title)
