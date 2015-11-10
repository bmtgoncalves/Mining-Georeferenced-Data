#!/usr/bin/env python

import urllib2
import posixpath
import foursquare
from foursquare_accounts import accounts

app = accounts["lyon"]

client = foursquare.Foursquare(client_id=app["client_id"],
                               client_secret=app["client_secret"])

client.set_access_token(app["access_token"])

url = "https://foursquare.com/tyayayayaa/checkin/5304b652498e734439d8711f?s=ScMqmpSLg1buhGXQicDJS4A_FVY&ref=tw"

parsed_url = urllib2.urlparse.urlparse(url)
checkin_id = posixpath.basename(parsed_url.path)
query = urllib2.urlparse.parse_qs(parsed_url.query)
screen_name = parsed_url.path.split('/')[1]

signature = query["s"][0]
source = query["ref"]

checkin = client.checkins(checkin_id, {"signature": signature})
