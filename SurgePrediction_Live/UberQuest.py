import csv
import requests
import time
import random


def uber_request(latitude, longitude, code='price', end_latitude=None, end_longitude=None):
    client_id = 'ADD'
    server_token = 'ADD'
    secret = 'ADD'

    price_parameters = {
        # 'client_id': client_id,
        'server_token': server_token,
        'client_secret': secret,
        'start_latitude': latitude,
        'start_longitude': longitude,
        'end_latitude': end_latitude,
        'end_longitude': end_longitude,
    }

    price_url = 'https://api.uber.com/v1/estimates/price'
    print('Getting price quote...')
    req_url = price_url
    response_price = requests.get(price_url, params=price_parameters)
    data_price = response_price.json()
    return data_price


#reading Taxi journey coords #
taxi_coords = []
with open('taxi_trips.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        taxi_coords.append([float(row['latitude']), float(row['longitude'])])

print('Number of Yellow Taxi journeys: ' + str(len(taxi_coords)))

f_out = open('UberQuestOutput.txt', 'w')

for i in range(0, 1000):
    coordsOrigin = random.choice(taxi_coords)
    coordsDestination = random.choice(taxi_coords)
    latitude_O = coordsOrigin[0]
    longitude_O = coordsOrigin[1]

    latitude_D = coordsDestination[0]
    longitude_D = coordsDestination[1]

    try:
        uber_response = uber_request(
            latitude_O, longitude_O, 'price', latitude_D, longitude_D)
    except:
        time.sleep(10.0)
        continue
    print >> f_out, str(
        (latitude_O, longitude_O, uber_response, latitude_D, longitude_D))
    print('Query retrieved, sleeping for a sec.')
    time.sleep(1.0)


f_out.close()

print('Uber Quest is Over.')
