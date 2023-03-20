# Welcome! This is a project created by three students, Tiffanie, William, and Joshua! Hopefully we'll help you decide on a place to eat.

import json
import googlemaps
import requests
from random import randint
import time
from dotenv import load_dotenv
import os
load_dotenv()

gmaps = googlemaps.Client(os.getenv('API_key'))

# km to meters - maximum radius for Places API is 50,000m
def km_to_meters(km):
    num = km * 1000
    if num > 50000:
        num = 50000
    return num

# Obtaining coordinates based on entered address
x = True
z = True
while x:
    address = input('Enter address: ')
    geocode_result = gmaps.geocode(address)
    for loc in geocode_result:
        location = loc['formatted_address']
        print('Entered address:', location)
    corr = input('Is this address correct (Y/N)? ')
    while z:
        if (corr == 'Y' or corr == 'y'):
            user_latitude = loc['geometry']['location']['lat']
            user_longitude = loc['geometry']['location']['lng']
            x = False
            z = False
        elif (corr == 'N' or corr == 'n'):
            break
        else:
            corr = input('Please enter Y/N: ')
    print()

# User inputs (price range, ratings, distance)
user_minprice = input('Enter minimum price range (0-4): ')
user_maxprice = input('Enter maximum price range (0-4): ')
user_km = int(input('How far are you willing to travel (km)? '))
user_radius = km_to_meters(user_km)
print()

# Define our Search
response = gmaps.places('restaurant', location=(user_latitude, user_longitude), radius=user_radius, min_price=user_minprice, max_price=user_maxprice, open_now=True)

# Filtering Json Data
results = response.get('results')

names = []
address = []
price = []
rating = []
total_ratings = []
counter = 0
for i in results:
    names.append(i['name'])
    address.append(i['formatted_address'])
    price.append(i['price_level'])
    rating.append(i['rating'])
    total_ratings.append(i['user_ratings_total'])

    if counter == 0:
        top_names = i['name']
        top_address = i['formatted_address']
        top_price = i['price_level']
        top_rating = i['rating']
        top_total_ratings = i['user_ratings_total']
    else:
        if i['rating'] > top_rating:
            top_names = i['name']
            top_address = i['formatted_address']
            top_price = i['price_level']
            top_rating = i['rating']
            top_total_ratings = i['user_ratings_total']
    counter += 1

if len(results) == 0:
       print('There are no results for your search.')
else:
    random = randint(0, len(results) - 1)
    print('Randomly selected restaurant:')
    print(names[random])
    print(address[random])
    print('Price Level:        {}'.format('$' * int(price[random])))
    print('Rating:             {:.1f}'.format(float(rating[random])))
    print('Total User Ratings: {:,}'.format(int(total_ratings[random])))
    print()

    print('Top Rated restaurant:')
    print(top_names)
    print(top_address)
    print('Price Level:        {}'.format('$' * int(top_price)))
    print('Rating:             {:.1f}'.format(float(top_rating)))
    print('Total User Ratings: {:,}'.format(int(top_total_ratings)))
    print()

    print('Don\'t like what you see? Take a look at all the restaurants nearby.')
    print()

for place in results:
    print(place['name'])
    print(place['formatted_address'])
    print('Price Level:        {}'.format('$' * int(place['price_level'])))
    print('Rating:             {:.1f}'.format(float(place['rating'])))
    print('Total User Ratings: {:,}\n'.format(int(place['user_ratings_total'])))

y = True
while y:
    try:
        time.sleep(2)
        response = gmaps.places(page_token = response['next_page_token'])
        results = response.get('results')
        for place in results:
            print(place['name'])
            print(place['formatted_address'])
            print('Price Level:        {}'.format('$' * int(place['price_level'])))
            print('Rating:             {:.1f}'.format(float(place['rating'])))
            print('Total User Ratings: {:,}\n'.format(int(place['user_ratings_total'])))
    except:
        y = False