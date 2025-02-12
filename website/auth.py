from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!!!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='danger')
        else:
            flash('Username does not exist.', category='danger')

    return render_template("login.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        password1 = data.get('password1')

        user = User.query.filter_by(username=username).first()

        if user:
            flash('User already exists.', category='danger')
        elif len(username) < 6:
            flash('Username must be greater than 6 characters.', category='danger')
        elif password != password1:
            flash('Passwords dont match', category='danger')
        elif len(password) < 8:
            flash('Password must be greater than 8 characters.', category='danger')
        else:
            #add user to database
            new_user = User(username=username, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()

            flash('User created!!!', category='success')
            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
