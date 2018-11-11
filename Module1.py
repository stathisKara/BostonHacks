# importing required libraries
from datetime import time
import requests
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
source = sys.argv[1]

# Take destination as input
dest = sys.argv[2]

# url variable store url
url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

# Get method of requests module
# return response object
print(url + 'origins=' + source +
                 '&destinations=' + dest +
                 '&key=' + api_key)
r = requests.get(url + 'origins=' + source +
                 '&destinations=' + dest +
                 '&key=' + api_key)

# json method of response object
# return json format result
x = r.json()

# bydefault driving mode considered

# print the vale of x
print(x)

# Requires API key
gmaps = googlemaps.Client(api_key)

# Requires cities name
my_dist = gmaps.distance_matrix(source, dest)['rows'][0]['elements'][0]["duration"]["value"]

def requestTime(origin, destination, arrival_time, departure_time=-1, mode='driving', api_key='AIzaSyCNBl9RA3jmY5dc3A7n4tksBXrMl4LjLFc'):
    '''
    takes as input:
    origin: string
    destination: string
    arrival_time: time in seconds since Epoch, int
    departure_time: time in seconds since Epoch, int
    mode: transport mode, 'transit' by default
    api_key: api key

    IF BOTH arrival_time and departure_time are provided,
    only take arrival time.

    Return:
    JSON response
    '''
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    requestUrl = url + 'origins=' + origin + '&destinations=' + destination + '&mode=' + mode + '&key=' + api_key
    # print(arrival_time)
    # print(departure_time)
    if arrival_time > 0:
        # print('arrival bigger')
        requestUrl += '&arrival_time=' + str(arrival_time)
        print(requestUrl)
    elif departure_time > 0:
        # print('depart bigger')
        requestUrl += '&departure_time=' + str(departure_time)
    else:
        pass
    # print(requestUrl)

    r = requests.get(requestUrl)
    x = r.json()
    return x


def smoothFit(x, y, n_neighbors = 30):
	'''
	takes as input, x, a list of time points in second,
	y: a list of times returned from google API, corresponding to a time point in x
	n_neighbors: number of neighbors to regress among
	Return:
	predictionPrediction: the predicted points
	'''

	neigh = KNeighborsRegressor(n_neighbors=n_neighbors)
	neigh.fit(x.reshape(-1, 1), y)
	prediction = neigh.predict(x.reshape(-1, 1))

	neigh.fit(x.reshape(-1, 1), prediction)
	predictionPrediction = neigh.predict(x.reshape(-1, 1))
	return x, predictionPrediction


# Printing the result
print(my_dist)
origin = sys.argv[1]
destination = sys.argv[2]
arrival_time = sys.argv[3]
ftr = [3600,60,1]
arrival_time = sum([a*b for a,b in zip(ftr, map(int,arrival_time.split(':')))])
print(arrival_time)
#print(requestTime(origin, destination, arrival_time))


current_time = datetime.datetime.now().time()
current_time = int(current_time.hour)*3600 + int(current_time.minute)*60 + int(current_time.second)
print(current_time)

Time_interval = arrival_time - current_time - my_dist
print(Time_interval)

if Time_interval <0:
    arrival_time = current_time+my_dist + 60
    Time_interval = arrival_time - current_time - my_dist
    print("You cannot get there that fast")
results = []
y = []
x = []
print(Time_interval)

for i in range(0, Time_interval, 600):
    results.append(requestTime(origin, destination, arrival_time, current_time +i*600))

for i in results :
    print('i')
    print(i['rows'][0]['elements'][0]["duration"]["value"])
    y.append(i['rows'][0]['elements'][0]["duration"]["value"])

for i in range(len(y)) :
    x.append(arrival_time - y[i])

smoothFit(x, y)
print(results)
print(x)
print(y)








sys.stdout.flush()

'''
Code below for converting seconds to timestamp format
Doesn't work


from_zone = tz.tzutc()
to_zone = tz.tzlocal()
#input
s = "11/11/2018"
f = "%d/%m/%Y  %H:%M:%S"
l = time.strftime(f, time.gmtime(my_dist))
#format
print(l)
utc = datetime.datetime.strptime(l, f)
utc = utc.replace(tzinfo=from_zone)
central = utc.astimezone(to_zone)
print(central)
# convert to seconds
#seconds = time.mktime(datetime.utc.astimezone(to_zone).timetuple())

#print(seconds)
#seconds convert back to string
#l = time.strftime(f, time.gmtime(seconds))

print(l)

'''