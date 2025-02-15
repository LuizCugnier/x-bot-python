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
        """Encrypts data before storing it in the database."""
        if isinstance(data, str):
            data = data.encode()  # Convert string to bytes
        encrypted_data = cipher.encrypt(data)
        return encrypted_data.decode()  # Convert bytes to string for storage

    def decrypt_data(self, encrypted_data):
        """Decrypts data for use."""
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()  # Convert string to bytes
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data.decode() 