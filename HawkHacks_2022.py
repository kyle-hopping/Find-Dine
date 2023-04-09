# Welcome! This is a project created by three students, Tiffanie, William, and Joshua! Hopefully we'll help you decide on a place to eat.

import json
import googlemaps
import requests
from random import randint
import time
from dotenv import load_dotenv
import os
import customtkinter

load_dotenv()

gmaps = googlemaps.Client(os.getenv('API_key'))

# km to meters - maximum radius for Places API is 50,000m
def km_to_meters(km):
    num = km * 1000
    if num > 50000:
        num = 50000
    return num

def test():
    #print(entry1.get(), op1.get(), op2.get(),entry2.get())
    # Obtaining coordinates based on entered address
    x = True
    z = True
    while x:
        address = addy.get() #input('Enter address: ')
        geocode_result = gmaps.geocode(address)
        for loc in geocode_result:
            location = loc['formatted_address']
            print('Entered address:', location)
        corr = 'Y' #input('Is this address correct (Y/N)? ')
        
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
    user_minprice =  min_pr.get() #input('Enter minimum price range (0-4): ')
    user_maxprice = max_pr.get() #input('Enter maximum price range (0-4): ')
    user_km = int(dist.get()) #int(input('How far are you willing to travel (km)? '))
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
    results_txt = ""
    if len(results) == 0:
        print('There are no results for your search.')
        results_txt = 'There are no results for your search.\n'
    else:
        random = randint(0, len(results) - 1)
        print('Randomly selected restaurant:')
        print(names[random])
        print(address[random])
        print('Price Level:        {}'.format('$' * int(price[random])))
        print('Rating:             {:.1f}'.format(float(rating[random])))
        print('Total User Ratings: {:,}'.format(int(total_ratings[random])))
        print()
        results_txt = 'Randomly selected restaurant: \n'   
        results_txt = results_txt + names[random] + "\n"
        results_txt = results_txt + address[random] + "\n"
        results_txt = results_txt + 'Price Level:        {}'.format('$' * int(price[random])) + "\n"
        results_txt = results_txt + 'Rating:             {:.1f}'.format(float(rating[random]))  + "\n"
        results_txt = results_txt + 'Total User Ratings: {:,}'.format(int(total_ratings[random])) + "\n"

        print('Recommended restaurant:')
        print(top_names)
        print(top_address)
        print('Price Level:        {}'.format('$' * int(top_price)))
        print('Rating:             {:.1f}'.format(float(top_rating)))
        print('Total User Ratings: {:,}'.format(int(top_total_ratings)))
        print()
        results_txt = 'Recommended restaurant: \n'   
        results_txt = results_txt + top_names + "\n"
        results_txt = results_txt + top_address + "\n"
        results_txt = results_txt + 'Price Level:        {}'.format('$' * int(top_price)) + "\n"
        results_txt = results_txt + 'Rating:             {:.1f}'.format(float(top_rating))  + "\n"
        results_txt = results_txt + 'Total User Ratings: {:,}'.format(int(top_total_ratings)) + "\n"


        print('Don\'t like what you see? Take a look at all the restaurants nearby.')
        print()

    for place in results:
        print(place['name'])
        print(place['formatted_address'])
        print('Price Level:        {}'.format('$' * int(place['price_level'])))
        print('Rating:             {:.1f}'.format(float(place['rating'])))
        print('Total User Ratings: {:,}\n'.format(int(place['user_ratings_total'])))
        results_txt = results_txt + "\n\n"
        results_txt = results_txt + place['name'] + "\n"
        results_txt = results_txt + place['formatted_address'] + "\n"
        results_txt = results_txt + 'Price Level:        {}'.format('$' * int(place['price_level'])) + "\n"
        results_txt = results_txt + 'Rating:             {:.1f}'.format(float(place['rating']))  + "\n"
        results_txt = results_txt + 'Total User Ratings: {:,}\n'.format(int(place['user_ratings_total'])) + "\n"


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
    frame2.pack(pady=40, padx= 30,side = "left" , fill="both" , expand=True)
    results = customtkinter.CTkLabel(master=frame2, text=results_txt)
    results.pack(padx = 12, pady = 10)


#start of GUI
root = customtkinter.CTk()
root.geometry("1100x650") #dimensions of screen
root.title("Find Restaurant") #name of application

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=40, padx= 30, side = "left", fill="both", expand=True) 
lable = customtkinter.CTkLabel(master=frame, text="Find Restaurant") #text_font=("Roboto", 24)
lable.pack(pady=12, padx = 10) 

addy = customtkinter.CTkEntry(master=frame, placeholder_text="Address", width=300)
addy.pack(pady = 20, padx = 10)

lable2 = customtkinter.CTkLabel(master=frame, text="Enter minimum price range")
lable2.pack(pady=12, padx = 10) 
min_pr = customtkinter.CTkOptionMenu(master=frame, values=["0","1","2","3","4"])
min_pr.pack(pady = 12, padx = 10)
min_pr.set("0")

lable3 = customtkinter.CTkLabel(master=frame, text="Enter maximum price range")
lable3.pack(pady=12, padx = 10) 
max_pr = customtkinter.CTkOptionMenu(master=frame, values=["0","1","2","3","4"])
max_pr.pack(pady = 12, padx = 10)
max_pr.set("0")

dist = customtkinter.CTkEntry(master=frame, placeholder_text="How far are you willing to travel (km)?", width=300)
dist.pack(pady = 12, padx = 10)

button = customtkinter.CTkButton(master=frame, text="Confirm", command=test, width=300)
button.pack(pady = 12, padx = 10)

frame2 = customtkinter.CTkScrollableFrame(master=root)
#frame2.pack(pady=40, padx= 30,side = "left" , fill="both" , expand=True)
results_txt = ""
#results = customtkinter.CTkLabel(master=frame2, text=results_txt)
#results.pack(padx = 12, pady = 10)

root.mainloop()
#end of GUI