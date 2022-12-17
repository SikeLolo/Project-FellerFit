from bs4 import BeautifulSoup
from googlesearch import search
import requests
from googleplaces import GooglePlaces, types, lang
import googlemaps
import requests
import json
from geopy.geocoders import Nominatim
import random
 
def price(site):
   soup = BeautifulSoup(requests.get(site).text, "html.parser")
   for txt in soup.select('div'):
       if "$" in txt.text:
           fill = (txt.text).replace(" ","")
           fill = fill.split()
           out = []
           for word in fill:
               if "$" in word and word != "$" and "." in word:
                   out.append(word)
           return out
   return "none"
 
def goog_search(prompt):
   results = search(prompt +" membership price")
   for site in results:
       data = price(site)
       if data != "none":
           return data
   return ["none"]
 
def nearby():
    API_KEY = 'AIzaSyA50LdIqws3j_NlKAJ4irrkaBPDqDqXwCA'
   
    google_places = GooglePlaces(API_KEY)
    gmaps = googlemaps.Client(API_KEY)
   
    # get address
    validaddress = True
    geolocator = Nominatim(user_agent="http")
    try:
        location = geolocator.geocode(input('Please enter your address: '))
    except:
        print('Not a valid address feller!')
        validaddress = False
    print((location.latitude, location.longitude))
   
    # getting all the gyms
    if validaddress is True:
        query_result = google_places.nearby_search(
                lat_lng ={'lat': location.latitude, 'lng': location.longitude},
                radius = ((int(input('Enter the maximum range from your home in kilometres: ')*1000))),
                types =[types.TYPE_GYM])
   
        # list of all the gyms
        gyms = {}
        for place in query_result.places:
            place.get_details()
   
            gyms[place.name] = []
            gyms[place.name].append(place.rating)
       
            try:
                distance = gmaps.distance_matrix(location, place.name)['rows'][0]['elements'][0]['distance']['text']
                duration = gmaps.distance_matrix(location, place.name)['rows'][0]['elements'][0]['duration']['text']
                gyms[place.name].append(distance)
                gyms[place.name].append(duration)
            except:
                pass
 
   
    opt_gym = "NA"
    accepted = ["1","2","3","4","5","6","7","8","9","0"]
    for gym in gyms:
        prices = goog_search(gym)
        cur = ""
        for info in prices:
            try:
                for char in range(info.find("$")+1,len(info)):
                    if char not in accepted:
                        break
                    else:
                        cur += char
            except: pass
        try: gyms[gym].append(float(cur))
        except: gyms[gym].append(float("inf"))
        print(gym,gyms[gym])
       
 
 
 
 
 
 
while 1:
   nearby()
   #print(gyms)
