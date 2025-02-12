import tweepy
import tweepy.errors
import time

BEARER_TOKEN = r'AAAAAAAAAAAAAAAAAAAAAIZRygEAAAAA88%2FurCPMghdCut2xw6JMeH0Ft1M%3DbkdGHIniVQI1y6VCuxbkZ0xDVFS2iDmRCNB71dfC4kH3boHr8p'
API_KEY = '3f3Lp2dJQjgrarkxUrBuT5ogv'
API_SECRET_KEY = 'USooIy2lJPRvOQr1Pt8xSJRKyCYDjz3KpZiBMKGlAi8Ji5la22'
ACCESS_TOKEN = '2375748896-QGMwdmsz7FvF8sglaUs49yg62MWhx9UcUIjWh0D'
ACCESS_TOKEN_SECRET = '65GanS5lymuQDDKRehQPZdRivj9fo03E6AasJd3bNVgcg'

BEARER_TOKEN2 = r'AAAAAAAAAAAAAAAAAAAAABxkzAEAAAAAzed22Oze0OM6V0Az1Jhc%2FZGqlsY%3DPM6ZWo0J42roXzjOckzsBl4DK8LdpfT0YJoOdiiBvGV6ES0Tam'
API_KEY2 = 'QfdJuAfjVUe2uQJ0eUaT3LEQN'
API_SECRET_KEY2 = 'zSnfvOj6VSnzUgb8qyHTDUrPAGG8zF4wVOWOsSNFzX2f53394I'
ACCESS_TOKEN2 = '1885440147879055360-hRU0UIFrWk9WqAUhkcyciPxYpwIgTa'
ACCESS_TOKEN_SECRET2 = 'ZlAO1WMWoE9WlUW5xgmTbuXHordAqmdxhzkW74rdZS2dN'

client = tweepy.Client(
    bearer_token=BEARER_TOKEN2,
    consumer_key=API_KEY2,
    consumer_secret=API_SECRET_KEY2,
    access_token=ACCESS_TOKEN2,
    access_token_secret=ACCESS_TOKEN_SECRET2
)

comment_text = "LFG!!!"

def process_tweet(tweet_url, comment_text):
    try:
        tweet_id = tweet_url.split("/")[-1]

        client.like(tweet_id)
        print("Tweet curtido com sucesso")

        client.retweet(tweet_id)
        print(f"Tweet retweetado {tweet_url}")

        client.create_tweet(text=comment_text, in_reply_to_tweet_id=tweet_id)
        print(f"Commented on tweet: {tweet_url}")

    except tweepy.errors.TweepyException as e:
        if "Too Many Requests" in str(e):
            # Extract the reset time from the error headers
            reset_time = int(e.response.headers.get('x-rate-limit-reset', 0))
            current_time = int(time.time())
            wait_time = reset_time - current_time

            if wait_time > 0:
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds...")
                time.sleep(wait_time)
                process_tweet(tweet_url, comment_text)  # Retry after waiting
            else:
                print("Rate limit exceeded. Please try again later.")
        else:
            print(f"Error: {e}")

tweet_url = "https://x.com/ishy9000/status/1886126422105948173"  # Replace with the tweet link
process_tweet(tweet_url, comment_text)