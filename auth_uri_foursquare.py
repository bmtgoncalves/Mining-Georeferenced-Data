#!/usr/bin/env python

import foursquare

accounts = {"tutorial": {"client_id": "CLIENT_ID",
                         "client_secret": "CLIENT_SECRET",
                         "access_token": ""
                         }
            }

app = accounts["tutorial"]

client = foursquare.Foursquare(client_id=app["client_id"],
                               client_secret=app["client_secret"],
                               redirect_uri='http://www.bgoncalves.com/redirect')

auth_uri = client.oauth.auth_url()
print auth_uri
