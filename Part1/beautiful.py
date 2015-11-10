#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import urllib2
import requests
import posixpath

url = "http://4sq.com/18aGENW"

headers = {"User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0"}

request = requests.get(url, headers=headers)

final_url = request.url
parsed = urllib2.urlparse.urlparse(final_url)
query = parsed.query
signature = urllib2.urlparse.parse_qs(query)["s"][0]

checkin_id = posixpath.basename(parsed.path)
user = posixpath.dirname(parsed.path).split('/')[1]

soup = BeautifulSoup(request.text)

venue_push = soup.div(attrs={"class": "venue push"})[0]
screen_name = venue_push.h1.strong.text

venue = venue_push.a["href"]

print "Checkin %s is for User \"%s\" with Name \"%s\" checking in at %s"\
    % (checkin_id, user, screen_name, posixpath.basename(venue))
