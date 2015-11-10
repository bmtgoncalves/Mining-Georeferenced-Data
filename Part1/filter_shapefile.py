#!/usr/bin/env python

import sys
import shapefile
from shapely.geometry import shape, Point
import gzip

shp = shapefile.Reader("nybb_15c/nybb_wgs84.shp")

print "Found", shp.numRecords, "records:"

pos = 2  # Manhattan

count = 0
for record in shp.records():
    print count, "  ", record[1]
    count += 1

print >> sys.stderr, "Using", shp.records()[pos][1], "..."

manhattan = shape(shp.shapes()[pos])

fp = gzip.open("Manhattan.json.gz", "w")

try:
    for line in gzip.open("NYC.json.gz"):
        try:
            tweet = eval(line.strip())

            if "coordinates" in tweet and tweet["coordinates"] is not None:
                point = Point(tweet["coordinates"]["coordinates"])

                if manhattan.contains(point):
                    print >> fp, line.strip()
        except:
            pass
except:
    pass

fp.close()
