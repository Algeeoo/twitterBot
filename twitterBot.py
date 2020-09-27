import tweepy
import logging
import time
import random
from datetime import datetime, timedelta


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

consumer_key = 'IR2LVH3EUav0xXVVWSTW1YCU0'
consumer_secret = 'pPty4ubsStrPvhJagVShnX0h4V3c4fiDA5v403LbQRKiVjwzcu' 

access_token = '1233683074417922049-MlNT1A0cy0j9LdtR2sV6fn7VZbS4mG' 
access_token_secret = 'MeD9KSgjiUZMZbkCxTruy1JSvtgH0pBwDYih27gVwAbUu' 


auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


        

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
                time.sleep(10)
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
                time.sleep(10)
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

def main(keywords):
    api = tweepy.API(auth)
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])
    

if __name__ == "__main__":
    main(["IFB"])


