from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json


ACCESS_TOKEN = '1217669196240379904-r6ITYlP5AJK7iHDY8lfILVoMr3tYoa'
ACCESS_SECRET = 'GbHe8b3NxEVZEJUI4dlY7mGfqx3zytRj3RTCpV6XD1KQ9'
API_KEY = '8fjdRalWa1SbfkZbBLbAgah9w'
API_SECRET = 'yzdedVz471O8aXMri5totyQAa2uKG6pzqXRgBXPmwN6M15JHb7'

tweet_count = 0
max_tweets = 10000


class TwitterListener(StreamListener):

    def on_data(self, tweet):
        global tweet_count
        global max_tweets
        global stream
        if tweet_count < max_tweets:
            try:
                tweet = tweet.strip()
                tweet_js = json.loads(tweet)
                if 'text' in tweet_js:
                    print(tweet)
                    tweet_count += 1
            except Exception as e:
                pass
            return True
        else:
            stream.disconnect()

    def on_error(self, status):
        print(status)
        return False


if __name__ == '__main__':
    auth = OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    twitterListener = TwitterListener()
    stream = Stream(auth, twitterListener)
    stream.sample()
