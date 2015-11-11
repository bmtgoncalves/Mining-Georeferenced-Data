# Mining Georeferenced Data: Location-based Services and the Sharing Economy
A hands on guide on using Python to collect, analyse and mine geo-referenced data from location based services (e.g. Foursquare, Twitter) and the Sharing Economy (Uber, Airbnb etc.). 

This code can be better understood following the slides below from the original presentation at the PyData NYC conference.

Part 1 Slides by Bruno Gonçalves: http://www.slideshare.net/bgoncalves/mining-georeferenced-data 

Part 2 Slides by Anastasios Noulas: http://www.slideshare.net/tnoulas/mining-georeferenced-data-locationbased-services-and-the-sharing-economy

## Contents

* Introduction to Twitter
* Registering a Twitter Application
* API Basics
* Streaming Geolocated Tweets [twitter](https://pypi.python.org/pypi/twitter)
* Filter Based on an arbitrary Polygon [shapely](https://pypi.python.org/pypi/Shapely), [shapefile](https://github.com/GeospatialPython/pyshp)
* Parse URLs [urlparse](https://docs.python.org/2/library/urlparse.html)
* Register a Foursquare Application
* Query Checkin Information [foursquare](https://github.com/mLewisLogic/foursquare)
* Parse webpages [requests](http://docs.python-requests.org/en/latest/), [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) and extract Checkin Information
* Place Networks [networkx](https://networkx.github.io/)
* Place Centrality
* Taxi Journeys [Basemap](http://matplotlib.org/basemap/)
* Querying Uber API
