import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#reading Taxi journey geographic coordinates #
taxi_coords = []
with open('taxi_trips.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		taxi_coords.append([float(row['latitude']), float(row['longitude'])])

y = [i[0] for i in taxi_coords]
x = [i[1] for i in taxi_coords]
colors = ['k' for i in range(0, len(y))]
popularities = [0.1 for i in range(0, len(y))]

m = Basemap(projection='merc',resolution='l',llcrnrlon=-74.0616,urcrnrlat=40.82,
urcrnrlon=-73.8563,llcrnrlat=40.699) #center map to NYC

# maps geocoordinates to pixel positions
x1,y1=m(x,y)
m.scatter(x1,y1,s=popularities,c=colors, marker="o",alpha=0.7)
plt.savefig('taxis.png')
plt.close()