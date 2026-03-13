# Python Script to Extract tweets of a 
# particular Hashtag using Tweepy and Pandas 


# import modules 
import pandas as pd 
import tweepy 
from PIL import Image
import urllib.request as urllib2


# function to display data of each tweet 
def printtweetdata(n, ith_tweet): 
	print() 
	print(f"Tweet {n}:") 
	print(f"Username:{ith_tweet[0]}") 
	print(f"Description:{ith_tweet[1]}") 
	print(f"Location:{ith_tweet[2]}") 
	print(f"Following Count:{ith_tweet[3]}") 
	print(f"Follower Count:{ith_tweet[4]}") 
	print(f"Total Tweets:{ith_tweet[5]}") 
	print(f"Retweet Count:{ith_tweet[6]}") 
	print(f"Tweet Text:{ith_tweet[7]}") 
	print(f"Hashtags Used:{ith_tweet[8]}") 
	print(f"Tweet ID:{ith_tweet[9]}") 
	print(f"Replies:{ith_tweet[11]}")
	
	images = ith_tweet[10]
	for image in images:
		media_url=image['media_url']
		print("Images: ", media_url)
		im = Image.open(urllib2.urlopen(media_url))
		#im.show()



# function to perform data extraction 
def scrape(words, date_since, numtweet): 
	
	# Creating DataFrame using pandas 
	db = pd.DataFrame(columns=['username', 'description', 'location', 'following', 
							'followers', 'totaltweets', 'retweetcount', 'text', 'hashtags','tweetID','images','replies',]) 
	
	# We are using .Cursor() to search through twitter for the required tweets. 
	# The number of tweets can be restricted using .items(number of tweets) 
	tweets = tweepy.Cursor(api.search, q=words, lang="en", 
						since='2021-01-01', 
						tweet_mode='extended',
						include_entities=True).items(numtweet) 
	
	# .Cursor() returns an iterable object. Each item in 
	# the iterator has various attributes that you can access to 
	# get information about each tweet 
	list_tweets = [tweet for tweet in tweets] 
	
	# Counter to maintain Tweet Count 
	i = 1
	
	# we will iterate over each tweet in the list for extracting information about each tweet 
	for tweet in list_tweets: 
		
		reply_tweets = tweepy.Cursor(api.search, q='to:{}'.format(user_name),
                                since_id=tweet.id, tweet_mode='extended').items()

		username = tweet.user.screen_name 
		description = tweet.user.description 
		location = tweet.user.location 
		following = tweet.user.friends_count 
		followers = tweet.user.followers_count 
		totaltweets = tweet.user.statuses_count 
		retweetcount = tweet.retweet_count 
		hashtags = tweet.entities['hashtags'] 
		images=tweet.entities['media']
		tweetId= tweet.id
		replies=[]
		while True:
			try:
				reply = reply_tweets.next()
				if not hasattr(reply, 'in_reply_to_status_id_str'):
					continue
				if reply.in_reply_to_status_id == tweetId:
					replies.append(reply.full_text)
					print("reply of tweet:{}".format(reply.full_text))

			except tweepy.RateLimitError as e:
				logging.error("Twitter api rate limit reached".format(e))
				time.sleep(60)
				continue

			except tweepy.TweepError as e:
				print("Tweepy error occured:{}".format(e))
				break

			except StopIteration:
				break

			except Exception as e:
				print("Failed while fetching replies {}".format(e))
				break
		

		# Retweets can be distinguished by a retweeted_status attribute, 
		# in case it is an invalid reference, except block will be executed 
		try: 
			text = tweet.retweeted_status.full_text 
		except AttributeError: 
			text = tweet.full_text 
		hashtext = list() 
		for j in range(0, len(hashtags)): 
			hashtext.append(hashtags[j]['text']) 
		

		# Here we are appending all the extracted information in the DataFrame 
		ith_tweet = [username, description, location, following, 
					followers, totaltweets, retweetcount, text, hashtext, tweetId, images,replies] 
		db.loc[len(db)] = ith_tweet 
		
		# Function call to print tweet data on screen 
		printtweetdata(i, ith_tweet) 

		i = i+1
	
	
	#Retweet solution:
	#api.update_status('The solution to the problem is: ', tweetId)

	#filename = 'scraped_tweets.csv'

	# we will save our database as a CSV file. 
	#db.to_csv(filename) 


if __name__ == '__main__': 
	
	# Enter your own credentials obtained 
	# from your developer account 
	consumer_key = "runsra61MhrLsjwgOYlANBzu9"
	consumer_secret = "fVChsb8y4Aq9zGqgYrINmza8klJobvkWhZdkXhZxhjxGGa4OMZ"
	access_key = "1364862750518730752-H5jTeNtJBbVxEg9iYpbZ3Ga7gZw5Oc"
	access_secret = "aOQS9MUKEJ6kpLTk5Na1XSdNdcAAuq0rdalF7Hz0lIaoa"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
	auth.set_access_token(access_key, access_secret) 
	api = tweepy.API(auth)
	user_name =  'xuxedu'
	
	# Enter Hashtag and initial date 
	words = "#save_my_plant" #Must include the pound(#) symbol to explicitly serach for only hashtags.
	print("Searching Twitter for tweets with HashTag: ", words) 
	date_since = '2021-01-01' #input() 
	print("Searching for Date since(The Tweets are required in yyyy-mm--dd)") 
	
	# number of tweets you want to extract in one run 
	numtweet = 5
	scrape(words, date_since, numtweet) 
	print('Scraping has completed!') 
