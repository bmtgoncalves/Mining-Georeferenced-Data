import twitter
from twitter_accounts import accounts
import urllib2

app = accounts["social"]

auth = twitter.oauth.OAuth(app["token"],
                           app["token_secret"],
                           app["api_key"],
                           app["api_secret"])

twitter_api = twitter.Twitter(auth=auth)

query = "foursquare"
count = 200

search_results = twitter_api.search.tweets(q=query, count=count)

statuses = search_results["statuses"]

while True:
    try:
        next_results = search_results["search_metadata"]["next_results"]

        args = urllib2.urlparse.parse_qs(next_results[1:])

        search_results = twitter_api.search.tweets(**args)
        statuses += search_results["statuses"]
    except:
        break
