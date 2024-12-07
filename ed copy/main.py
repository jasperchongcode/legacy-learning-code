import pandas as pd
import googlemaps
from itertools import tee
import numpy as np
import requests

#Perform request to use the Google Maps API web service
API_key = 'AIzaSyDEmF3tz8WtQVJn6Ato4AaqVzXpyD7sFKk'#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)

def min_distance(origins, destination = "Fertility North, Private Hospital, Suite 30, Level 2/60 Shenton Ave, Joondalup WA 6027"):
    destination= "place_id:"+"ChIJ9w4hEF9TzSsRoeIPfapxPGk"
    origins = "place_id:"+placeID(origins)
    result = gmaps.directions(origins, destination, alternatives=True)
    smallest = np.inf
    for r in result:
        string = r['legs'][0]['distance']['text']
        smallest = min(smallest, float(string.replace(" km","").replace(",","")))
    return smallest

def placeID(origins):
    # Just include "76 STATION AT..." in the beginning of your text query.
    ad = origins

    address = ad.replace(' ', '%20') # make sure there are no blank spaces for the URL
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+ address + \
        "&inputtype=textquery&fields=place_id&key="+ API_key
    response = requests.get(url).json()

    # place_ids = [] # container for place_id
    # for c in response['candidates']:
    #      place_ids.append(c)
    # place_ids[0]
    return response['candidates'][0]['place_id']


df = pd.read_csv('bvc.csv', names=['1','2','3','4','5'])
addresses = pd.Series(df.fillna('').values.tolist()).map(lambda x: ', '.join(map(str,x)))

out = []
for origin in addresses:
    out.append(min_distance(origin))
df['distance'] = out
print(df)