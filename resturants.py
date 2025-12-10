import requests
import json


def restaurants_places(api_key, long, lat, cuisine):

    base = 'https://api.geoapify.com/v2/places?'
    params = {
        'apiKey': api_key,
        'categories': 'catering.restaurant',
        'filter': f'circle:{long}, {lat}, 5000',
        'bias': f'proximity: {long}, {lat}',
    }

    response = requests.get(base, params=params)
    info = response.json()

    features = info.get('features', [])

    #need to add properties code
    #make sure open weather code stores long and lat values
    #to use here