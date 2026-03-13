"""
This script extracts tweets, metadata, images, and replies related to plant disease
queries posted by farmers using the hashtag #save_my_plant.
"""

import os
import time
import logging
import pandas as pd
import tweepy
from PIL import Image
import urllib.request as urllib2


# Twitter Authentication
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_key = os.getenv("TWITTER_ACCESS_KEY")
access_secret = os.getenv("TWITTER_ACCESS_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Printing Tweet Data
def printtweetdata(n, tweet_data):

    print(f"\nTweet {n}")
    print(f"Username: {tweet_data[0]}")
    print(f"Description: {tweet_data[1]}")
    print(f"Location: {tweet_data[2]}")
    print(f"Following Count: {tweet_data[3]}")
    print(f"Follower Count: {tweet_data[4]}")
    print(f"Total Tweets: {tweet_data[5]}")
    print(f"Retweet Count: {tweet_data[6]}")
    print(f"Tweet Text: {tweet_data[7]}")
    print(f"Hashtags Used: {tweet_data[8]}")
    print(f"Tweet ID: {tweet_data[9]}")
    print(f"Replies: {tweet_data[11]}")

    images = tweet_data[10]

    for image in images:

        media_url = image['media_url']
        print("Image URL:", media_url)

        try:
            Image.open(urllib2.urlopen(media_url))
        except:
            print("Could not load image")

# Tweet Scraper
def scrape(hashtag, since_date, num_tweets):

    db = pd.DataFrame(columns=[
        'username',
        'description',
        'location',
        'following',
        'followers',
        'totaltweets',
        'retweetcount',
        'text',
        'hashtags',
        'tweetID',
        'images',
        'replies'
    ])

    tweets = tweepy.Cursor(
        api.search,
        q=hashtag,
        lang="en",
        since=since_date,
        tweet_mode='extended',
        include_entities=True
    ).items(num_tweets)

    i = 1

    for tweet in tweets:

        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count

        hashtags = tweet.entities.get('hashtags', [])
        images = tweet.entities.get('media', [])

        tweetId = tweet.id
        replies = []

        try:

            reply_tweets = tweepy.Cursor(
                api.search,
                q=f"to:{username}",
                since_id=tweetId,
                tweet_mode='extended'
            ).items()

            while True:

                reply = next(reply_tweets)

                if reply.in_reply_to_status_id == tweetId:
                    replies.append(reply.full_text)

        except StopIteration:
            pass

        except tweepy.RateLimitError:
            logging.warning("Rate limit reached. Sleeping for 60 seconds.")
            time.sleep(60)

        except Exception as e:
            print("Error fetching replies:", e)

        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text

        hashtext = [tag['text'] for tag in hashtags]

        tweet_data = [
            username,
            description,
            location,
            following,
            followers,
            totaltweets,
            retweetcount,
            text,
            hashtext,
            tweetId,
            images,
            replies
        ]

        db.loc[len(db)] = tweet_data

        printtweetdata(i, tweet_data)

        i += 1

    db.to_csv("scraped_tweets.csv", index=False)

    print("\nScraping completed. Data saved to scraped_tweets.csv")


# Main 
if __name__ == '__main__':

    hashtag = "#save_my_plant -filter:retweets"
    since_date = "2021-01-01"
    num_tweets = 20

    print("Searching Twitter for hashtag:", hashtag)

    scrape(hashtag, since_date, num_tweets)
