import twitter
from twitter_accounts import accounts

app = accounts["social"]

auth = twitter.oauth.OAuth(app["token"], 
                           app["token_secret"], 
                           app["api_key"], 
                           app["api_secret"])

twitter_api = twitter.Twitter(auth=auth)

screen_name = "jabawack"

tweets = []

args = { "count" : 200,
         "trim_user": "true",
         "include_rts": "true"
        }

tweets = twitter_api.statuses.user_timeline(screen_name = screen_name, **args)

tweets_new = tweets

while len(tweets_new) > 0:
    max_id = tweets[-1]["id"] - 1
    tweets_new = twitter_api.statuses.user_timeline(screen_name = screen_name, max_id=max_id, **args)
    tweets += tweets_new

print "Found", len(tweets), "tweets"
