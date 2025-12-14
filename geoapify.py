import requests
import sqlite3
from api_key import geoapify_api_places

limit = 25
new_restaurants = 0

city_locations = [
    ("Detroit", 42.3314, -83.0458),
    ("Chicago", 41.8781, -87.6298),
    ("New York", 40.7128, -74.0060),
    ("Los Angeles", 34.0522, -118.2437),
    ("Houston", 29.7604, -95.3698),
    ("Seattle", 47.6062, -122.3321),
    ("Miami", 25.7617, -80.1918),
    ("Denver", 39.7392, -104.9903)
]
#need to fix this
def offset_restaurants(): #pagination #avoid duplicates
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM restaurants")
    offset = cur.fetchone()[0]
    conn.close()
    return offset
def get_cuisine(cur, cuisine): #add into cuisine table
    cur.execute("INSERT OR IGNORE INTO cuisines (name) VALUES (?)", (cuisine,))
    cur.execute("SELECT id FROM cuisines WHERE name=?", (cuisine,))
    c_result = cur.fetchone()[0]
    return c_result

conn = sqlite3.connect("project.db")
cur = conn.cursor()

for city_name, lat, lon in city_locations:
    if new_restaurants>=limit:
        break

    cur.execute("INSERT OR IGNORE INTO cities (name) VALUES (?)", (city_name,))
    cur.execute("SELECT id FROM cities WHERE name=?", (city_name,))
    city_id = cur.fetchone()[0]

    base = 'https://api.geoapify.com/v2/places?'
    params = {
        "categories": "catering.restaurant",
        "filter": f"circle:{lat},{lon},50000", #ann arbor latitude and longitude
        "offset": offset_restaurants(),
        "apiKey": geoapify_api_places,
        "limit": limit
    }
    response = requests.get(base, params=params)
    info = response.json()
    places = info.get('features', [])

    for place in places:
        if new_restaurants>=limit:
              break
        properties = place["properties"]
        cuisine_name = properties.get("cuisine", "Unknown")
        cuisine_id = get_cuisine(cur, cuisine_name)

        cur.execute("""
        INSERT OR IGNORE INTO restaurants
        (geoapify_id, name, city_id, cuisine_id, latitude, longitude, distance)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (properties["place_id"], properties.get("name", "Unknown"),
        city_id, cuisine_id, properties["lat"], properties["lon"], properties.get("distance", 0)))

        cur.execute("SELECT changes()")
        if cur.fetchone()[0]==1:
            new_restaurants +=1
    
conn.commit()
cur.execute("SELECT COUNT(*) FROM restaurants")
print(cur.fetchone()[0])
conn.close()
print("Data from Geoapify has been stored.")
