# importing required libraries
from datetime import time
import requests
import numpy
import json
import googlemaps
import datetime
import time
from dateutil import tz
import sys
from sklearn.neighbors import KNeighborsRegressor

# enter your api key here
api_key = 'AIzaSyCNBl9RA3jmY5dc3A7n4tksBXrMl4LjLFc'

# Take source as input
source = 'Boston'#sys.argv[1]

# Take destination as input
dest = 'nyc'#sys.argv[2]

# url variable store url
url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

# Get method of requests module
# return response object

r = requests.get(url + 'origins=' + source +
                 '&destinations=' + dest +
                 '&key=' + api_key)

# json method of response object
# return json format result
x = r.json()


# Requires API key
gmaps = googlemaps.Client(api_key)

# Requires cities name
my_dist = gmaps.distance_matrix(source, dest)['rows'][0]['elements'][0]["duration"]["value"]

def requestTime(origin, destination, arrival_time, departure_time=-1, mode='driving', api_key='AIzaSyCNBl9RA3jmY5dc3A7n4tksBXrMl4LjLFc'):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    requestUrl = url + 'origins=' + origin + '&destinations=' + destination + '&mode=' + mode + '&key=' + api_key
    # print(arrival_time)
    # print(departure_time)
    if arrival_time > 0:
        # print('arrival bigger')
        requestUrl += '&arrival_time=' + str(arrival_time)
    elif departure_time > 0:
        # print('depart bigger')
        requestUrl += '&departure_time=' + str(departure_time)
    else:
        pass
    # print(requestUrl)

    r = requests.get(requestUrl)
    x = r.json()
    return x


def smoothFit(x, y, n_neighbors = 2):
    x = numpy.array(x)
    neigh = KNeighborsRegressor(n_neighbors=n_neighbors)
    neigh.fit(x.reshape(-1, 1), y)
    prediction = neigh.predict(x.reshape(-1, 1))
    neigh.fit(x.reshape(-1, 1), prediction)
    predictionPrediction = neigh.predict(x.reshape(-1, 1))
    return x, predictionPrediction



origin = 'boston'#sys.argv[1]
destination = 'nyc' #sys.argv[2]
arrival_time = '13:30:00'#sys.argv[3]
ftr = [3600,60,1]
arrival_time = sum([a*b for a,b in zip(ftr, map(int,arrival_time.split(':')))])

current_time = datetime.datetime.now().time()
current_time = int(current_time.hour)*3600 + int(current_time.minute)*60 + int(current_time.second)

Time_interval = arrival_time - current_time - my_dist


if Time_interval <0:
    arrival_time = current_time+my_dist + 60
    Time_interval = arrival_time - current_time - my_dist
    #"You cannot get there that fast"

results = []
y = []
x = []

for i in range(0, Time_interval, 600):
    results.append(requestTime(origin, destination, arrival_time, current_time +i*600))

for i in results :
    y.append(i['rows'][0]['elements'][0]["duration"]["value"])

for i in range(len(y)) :
    x.append(arrival_time - y[i])

smoothFit(x,y)
sys.stdout.flush()
