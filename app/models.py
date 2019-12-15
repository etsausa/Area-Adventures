from datetime import datetime
from hashlib import md5
from app import db, ma
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
    #last_seen = db.Column(db.DateTime, default=datetime.utcnow())


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    description = db.Column(db.String(512), index=True)
    Long = db.Column(db.Float, index=True)
    Lat = db.Column(db.Float, index=True)
    timeStamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_submitted = db.Column(db.Boolean)
    user_id =  db.Column(db.Integer, db.ForeignKey(User.id))

    def __repr__(self):
        return '<Post {}>'.format(self.title)


#Marshmallow Schemas for JSONIFY
class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post
