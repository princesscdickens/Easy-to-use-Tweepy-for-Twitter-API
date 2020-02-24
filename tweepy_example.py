import tweepy
#import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
#from pymongo import MongoClient

# Step 1: Create a Twitter Dev account
# Step 2: Create an application to generate API keys and secrets
# Step 3: FILL IN THIS PART, replacing the '#' with your API keys
api_key = '#'
api_secret = '#'
access_token = '#'
access_secret = '#'
# Step 4: Decide which keywords you will use for searching and fill them in on line 69

# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        #print(status.id_str)
        
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")
        
        
        # check if text has been truncated
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text
        
        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            if hasattr(status.quoted_status,"extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text
        
        # remove characters that might cause problems with csv encoding        
        remove_characters = [",", "\n"]
        for c in remove_characters:
            text.replace(c," ")
            quoted_text.replace(c," ")
        
        with open("out.csv", "a", encoding='utf-8') as f:
            f.write("%s,%s,%s,%s,%s,%s\n" % (status.created_at,status.user.screen_name,is_retweet,is_quote,text,quoted_text))      
        
    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()
        
if __name__ == "__main__":

    # complete authorization abnd intialize API endpoint
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    
    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth = api.auth, listener=streamListener, tweet_mode='extended')
    
    with open("out.csv", "w", encoding='utf-8') as f:
        f.write("date,user,is_retweet,is_quote,text,quoted_text\n")

    # ADD KEYWORDS HERE - Example keywords: pitbull, pit bull, nanny dog
    tags = ["pitbull", "pit bull", "nanny dog"]
    stream.filter(track=tags)

# RUN THIS CODE WITH $ python3 tweepy_example.py