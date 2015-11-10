#!/usr/bin/env python

import foursquare
from foursquare_accounts import accounts

app = accounts["tutorial"]

client = foursquare.Foursquare(client_id=app["client_id"],
                               client_secret=app["client_secret"])

client.set_access_token(app["access_token"])

venue_id = "43695300f964a5208c291fe3"
venue = client.venues(venue_id)
similar = client.venues.similar(venue_id)

print "Similar venues to", venue["venue"]["name"], "(", venue["venue"]["hereNow"]["summary"], ")"
print
for venue in similar["similarVenues"]["items"]:
    print venue["name"]
