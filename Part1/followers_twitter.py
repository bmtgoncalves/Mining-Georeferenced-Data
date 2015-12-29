import twitter
from twitter_accounts import accounts

app = accounts["social"]

auth = twitter.oauth.OAuth(app["token"], 
                           app["token_secret"], 
                           app["api_key"], 
                           app["api_secret"])

twitter_api = twitter.Twitter(auth=auth)

screen_name = "stephen_wolfram"

cursor = -1
followers = []

while cursor != 0:
    result = twitter_api.followers.ids(screen_name=screen_name, cursor=cursor)

    followers += result["ids"]
    cursor = result["next_cursor"]

print "Found", len(followers), "Followers"