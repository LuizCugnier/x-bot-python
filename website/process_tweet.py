import tweepy
import time
from .models import db, TwitterAccounts
from cryptography.fernet import InvalidToken

def process_tweet(tweet_url, comment_text, account):
    print("Entering process_tweet function")  # Debug print
    try:
        access_token = account.decrypt_data(account.access_token)
        access_token_secret = account.decrypt_data(account.access_token_secret)
        consumer_key = account.decrypt_data(account.api_key)
        consumer_secret = account.decrypt_data(account.api_key_secret)
        bearer_token = account.decrypt_data(account.bearer_token)

        print(f"Access Token: {access_token}")
        print(f"Access Token Secret: {access_token_secret}")
        print(f"Consumer Key: {consumer_key}")
        print(f"Consumer Secret: {consumer_secret}")
        print(f"Bearer Token: {bearer_token}")

        client = tweepy.Client(
            access_token=access_token,
            access_token_secret=access_token_secret,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            bearer_token=bearer_token,
        )

        tweet_id = tweet_url.split("/")[-1]
        print(f"Tweet ID: {tweet_id}")

        # Like the tweet
        like_response = client.like(tweet_id)
        if like_response.data:
            print(f"Tweet curtido com sucesso pela conta {account.account_name}")
        else:
            print(f"Failed to like tweet: {like_response}")

        # Retweet the tweet
        retweet_response = client.retweet(tweet_id)
        if retweet_response.data:
            print(f"Tweet retweetado pela conta {account.account_name}")
        else:
            print(f"Failed to retweet: {retweet_response}")

        # Comment on the tweet
        comment_response = client.create_tweet(text=comment_text, in_reply_to_tweet_id=tweet_id)
        if comment_response.data:
            print(f"Comentário postado pela conta {account.account_name}")
        else:
            print(f"Failed to comment: {comment_response}")

    except InvalidToken as e:
        print(f"Decryption error: {e}")
    except tweepy.errors.TweepyException as e:
        if "Too Many Requests" in str(e):
            reset_time = int(e.response.headers.get('x-rate-limit-reset', 0))
            current_time = int(time.time())
            wait_time = reset_time - current_time

            if wait_time > 0:
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds...")
                time.sleep(wait_time)
                process_tweet(tweet_url, comment_text, account)  # Retry after waiting
            else:
                print("Rate limit exceeded. Please try again later.")
        else:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")