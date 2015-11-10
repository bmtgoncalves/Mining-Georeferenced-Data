#!/usr/bin/env python

import sys
import shapefile
from shapely.geometry import shape

shp = shapefile.Reader(sys.argv[1])

print "Found", shp.numRecords, "records:"

pos = None
count = 0
for record in shp.records():
    print "  ", record[1]

    if record[1] == sys.argv[2]:
        pos = count

    count += 1

if pos is None:
    print >> sys.stderr, sys.argv[2], "not found in shapefile"
    sys.exit()

print >> sys.stderr, "Using", sys.argv[2], "..."

manhattan = shape(shp.shapes()[pos])

print manhattan.contains(manhattan.centroid)
