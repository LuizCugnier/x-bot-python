from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import db, TwitterAccounts, User
from .process_tweet import process_tweet

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        data = request.form
        tweet_url = data["tweet_url"]
        comment_text = data["comment_text"]
        account_name = data["account"]
        account = TwitterAccounts.query.filter_by(account_name=account_name).first()


        if account:
            print(f"Account Found: {account.account_name}")
            print(f"Account Found: {account.access_token}")
            process_tweet(tweet_url, comment_text, account)
            flash("Tweet processed successfully!", "success")
        else:
            flash("Invalid account.", "error")

        return redirect(url_for("views.home"))
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