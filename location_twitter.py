#!/usr/bin/env python

import twitter
from twitter_accounts import accounts
import sys
import gzip

app = accounts["social"]

auth = twitter.oauth.OAuth(app["token"],
                           app["token_secret"],
                           app["api_key"],
                           app["api_secret"])

stream_api = twitter.TwitterStream(auth=auth)

query = "-74,40,-73,41"  # NYC

stream_results = stream_api.statuses.filter(locations=query)

tweet_count = 0

fp = gzip.open("NYC.json.gz", "a")

for tweet in stream_results:
    try:
        tweet_count += 1
        print tweet_count, tweet["id"]

        print >> fp, tweet
    except:
        pass

    if tweet_count % 10000 == 0:
        print >> sys.stderr, tweet_count
        break
