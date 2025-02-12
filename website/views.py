from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import db, TwitterAccounts, User
from cryptography.fernet import Fernet

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    accounts = TwitterAccounts.query.all() 
    return render_template("index.html", user=current_user, accounts=accounts)

@views.route('/register-x-account', methods=['GET', 'POST'])
@login_required
def register_x_account():
    if request.method == 'POST':
        data = request.form

        new_account = TwitterAccounts(
            account_name=data['account_name'],
            access_token=TwitterAccounts.encrypt_data(TwitterAccounts, data['access_token']),
            access_token_secret=TwitterAccounts.encrypt_data(TwitterAccounts, data['access_token_secret']),
            api_key=TwitterAccounts.encrypt_data(TwitterAccounts, data['api_key']),
            api_key_secret=TwitterAccounts.encrypt_data(TwitterAccounts, data['api_key_secret']),
            bearer_token=TwitterAccounts.encrypt_data(TwitterAccounts, data['bearer_token']),
            user_id=current_user.id
        )

        db.session.add(new_account)
        db.session.commit()
        flash("X Account registered successfully!", "success")
        return redirect(url_for('views.home'))

    return render_template("register-x-account.html", user=current_user)

@views.route('/registered-x-accounts')
@login_required
def registered_x_accounts():
    accounts = TwitterAccounts.query.join(User).all()
    
    return render_template("registered-x-accounts.html", user=current_user, accounts=accounts)