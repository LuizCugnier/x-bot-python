from . import db
from flask_login import UserMixin
from cryptography.fernet import Fernet
import os

FERNET_KEY = os.environ.get("FERNET_KEY") or Fernet.generate_key()
if not FERNET_KEY:
    raise ValueError("FERNET_KEY not found in environment variables.")
    
# Initialize the Fernet cipher
try:
    cipher = Fernet(FERNET_KEY)  # Encode to bytes
except ValueError as e:
    raise ValueError("Invalid FERNET_KEY. Ensure it is a 32-byte URL-safe base64-encoded string.") from e


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(500))
    twitter_accounts = db.relationship('TwitterAccounts', backref='user', lazy=True)

class TwitterAccounts(db.Model):
    __tablename__ = 'twitter_accounts'
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(150))
    access_token = db.Column(db.String(250))
    access_token_secret = db.Column(db.String(250))
    api_key = db.Column(db.String(250))
    api_key_secret = db.Column(db.String(250))
    bearer_token = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

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