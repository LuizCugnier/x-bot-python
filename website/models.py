from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    twitter_accounts = db.relationship('TwitterAccounts', backref='user', lazy=True)

class TwitterAccounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acces_token = db.Column(db.String(250))
    acces_token_secret = db.Column(db.String(250))
    api_token = db.Column(db.String(250))
    api_token_secret = db.Column(db.String(250))
    beare_token = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))