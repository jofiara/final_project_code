import requests
import sqlite3
from api_key import geoapify_api_places

limit = 25

def offset_restaurants(): #pagination #avoid duplicates
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM restaurants")
    offset = cur.fetchone()[0]
    conn.close()
    return offset


conn = sqlite3.connect("project.db")
cur = conn.cursor()

cur.execute("SELECT id, name FROM cuisines")
cuisines = cur.fetchall()

for cuisine_id, cuisine_name in cuisines:
    base = 'https://api.geoapify.com/v2/places?'
    params = {
        "categories": "catering.restaurant",
        "filter": "circle:-83.7430,42.2808,10000", #ann arbor latitude and longitude
        "offset": offset_restaurants(),
        "apiKey": geoapify_api_places,
        "limit": limit
    }
    response = requests.get(base, params=params)
    info = response.json()

    places = info.get('features', [])

    for place in places:
        properties = place["properties"]
        city = properties.get("city", "Unknown")

        cur.execute("INSERT OR IGNORE INTO cities (name) VALUES (?)", (city,))
        cur.execute("SELECT id FROM cities WHERE name=?", (city,))
        city_id = cur.fetchone()[0]

        cur.execute("""
        INSERT OR IGNORE INTO restaurants
        (geoapify_id, name, city_id, cuisine_id, latitude, longitude, distance)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (properties["place_id"], properties.get("name", "Unknown"),
        city_id, cuisine_id, properties["lat"], properties["lon"], properties.get("distance", 0)))

conn.commit()
conn.close()
print("Data from Geoapify has been stored.")
