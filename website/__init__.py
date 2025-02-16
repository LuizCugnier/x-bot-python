from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from cryptography.fernet import Fernet

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    fernet_key = os.environ.get('FERNET_KEY')
    if not fernet_key:
        # Generate a new Fernet key if not provided
        fernet_key = Fernet.generate_key().decode()  # Decode to string
    app.config['FERNET_KEY'] = fernet_key
    
    db.init_app(app)

    Bootstrap4(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    migrate.__init__(app, db)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, TwitterAccounts

    return app
