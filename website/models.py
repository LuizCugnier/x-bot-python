from . import db
from flask_login import UserMixin
from cryptography.fernet import Fernet
import os

SECRET_KEY = os.environ.get("SECRET_KEY") or Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    twitter_accounts = db.relationship('TwitterAccounts', backref='user', lazy=True)

class TwitterAccounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(150))
    access_token = db.Column(db.String(250))
    access_token_secret = db.Column(db.String(250))
    api_key = db.Column(db.String(250))
    api_key_secret = db.Column(db.String(250))
    bearer_token = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def encrypt_data(self, data):
        """Criptografa um valor antes de armazená-lo"""
        return cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, data):
        """Descriptografa um valor para uso"""
        return cipher.decrypt(data.encode()).decode()