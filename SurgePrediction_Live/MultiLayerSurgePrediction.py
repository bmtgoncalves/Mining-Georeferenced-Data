import csv
import numpy as np

lonMin = -74.1  # minimum longitude
lonMax = -73.7
lonStep = 0.0025  # defines cell size

latMin = 40.6  # minimum latitude
latMax = 41.0
latStep = 0.0025  # defines cell size

latLen = int((latMax - latMin) / latStep) + 1  # number of cells on the y-axis
lonLen = int((lonMax - lonMin) / lonStep) + 1  # number of cells on the x-axis

# Cell counts for each source of geo-data
FSQcellCount = np.zeros((latLen, lonLen))
AIRcellCount = np.zeros((latLen, lonLen))
TAXIcellCount = np.zeros((latLen, lonLen))


####### LOADING COORDS FROM 3 GEO LAYERS #########
airbnb_coords = []

with open('listings_sample.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        airbnb_coords.append([float(row['latitude']), float(row['longitude'])])

print('Number of Airbnb listings: ' + str(len(airbnb_coords)))


#reading Foursquare venue data #
foursquare_coords = []
with open('venue_data_4sq_newyork_anon.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        foursquare_coords.append(
            [float(row['latitude']), float(row['longitude'])])

print('Number of Foursquare listings: ' + str(len(foursquare_coords)))

#reading Taxi journey coords #
taxi_coords = []
with open('taxi_trips.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        taxi_coords.append([float(row['latitude']), float(row['longitude'])])

print('Number of Yellow Taxi journeys: ' + str(len(taxi_coords)))

############ ############ ############ ############

all_coords = [foursquare_coords, airbnb_coords, taxi_coords]
for i in range(0, 3):
    current_coords = all_coords[i]

    for coords in current_coords:
        lat = coords[0]
        longit = coords[1]

        # if outside the grid then ingore point
        if (lat < latMin) or (lat > latMax) or (longit < lonMin) or (longit > lonMax):
            continue

        # if outside the grid then ingore point
        cx = int((longit - lonMin) / lonStep)
        cy = int((lat - latMin) / latStep)

        if i == 0:
            FSQcellCount[cy, cx] += 1
        elif i == 1:
            AIRcellCount[cy, cx] += 1
        else:
            TAXIcellCount[cy, cx] += 1


# Load Area Average Surge: assume you have queried previously the UBER API
# and have collected info on pricing for an area
latLongSurge = {}
for l in open('averageSurgeInCell.csv', 'r'):
    splits = l.split(',')
    cy = int(splits[0])
    cx = int(splits[1])
    averageSurgeCoeff = float(splits[2])

    latLongSurge.setdefault(cy, {})
    latLongSurge[cy][cx] = averageSurgeCoeff

###################
import pylab as plt
surgeValues = [latLongSurge[cy][cx] for cy in range(
    0, latLen - 1) for cx in range(0, lonLen - 1) if latLongSurge[cy][cx] != 0]

plt.hist(surgeValues, color='yellow', bins=60,
         label='Surge Multipliers', alpha=0.8)
plt.ylabel('Frequency')
plt.xlabel('Area Mean Surge Multiplier')

vals = ['1.0', '1.05', '1.1', '1.15', '1.2',
        '1.25', '1.3', '1.35', '1.4', '1.45']
plt.xticks([1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3,
            1.35, 1.4, 1.45], vals, fontsize=10)


plt.grid(True)
plt.savefig('surgeMultDistribution.pdf')
plt.close()
###################


#### SURGE PREDICTOR ####
import scipy.stats as stats


yellows = [TAXIcellCount[cy][cx] for cy in range(
    0, latLen - 1) for cx in range(0, lonLen - 1) if latLongSurge[cy][cx] != 0]
places = [FSQcellCount[cy][cx] for cy in range(
    0, latLen - 1) for cx in range(0, lonLen - 1) if latLongSurge[cy][cx] != 0]
listings = [AIRcellCount[cy][cx] for cy in range(
    0, latLen - 1) for cx in range(0, lonLen - 1) if latLongSurge[cy][cx] != 0]

cnt = 0
labels = ['Yellow Taxis', 'Foursquare Places', 'Airbnb Listings']
print(len(surgeValues))
print(len(yellows))
for predictor in [yellows, places, listings]:
    r, p_value = stats.pearsonr(surgeValues, predictor)
    print(labels[cnt])
    print(r)
    print('---')
    cnt += 1

### SUPERVISED LEARNING FOR SURGE PREDICTION###

from sklearn import tree
y_train = []  # a list for your training labels
X_train = []  # feature values go here
for i in range(0, len(surgeValues)):
    y_train.append(surgeValues[i])
    X_train.append([yellows[i], listings[i], places[i]])

print('Training Decision Tree Regressor..')
###  Training and Testing: LEAVE ONE OUT ERROR ####
# Leave one out error has been considered as an unbiased estimator of the
# generalisation error ###
super_predictions = []
for i in range(0, len(surgeValues)):
    training_data_X = X_train[:i] + X_train[i + 1:]
    label_data_Y = y_train[:i] + y_train[i + 1:]
    NX_train = []
    ny_train = []
    for j in range(0, len(label_data_Y)):
        if label_data_Y[j] == 1.0:
            continue
        else:
            NX_train.append(X_train[j])
            ny_train.append(y_train[j])

    clf = tree.DecisionTreeRegressor(max_depth=30).fit(NX_train, ny_train)
    super_predictions.append(clf.predict([X_train[i]])[0])

r, p_value = stats.pearsonr(surgeValues, super_predictions)
print('Decision Tree Supervised Learning Regressor, r :' + str(r))
