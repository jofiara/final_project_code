import requests
import sqlite3
from api_key import open_weather_api

limit = 25

city_bank = ["Detroit", "Chicago", "Los Angeles", "New York", "Miami", "Seattle", "Boston",
             "Houston", "Phoenix", "San Francisco", "San Diego", "Dallas", "Philadelphia",
            "Atlanta", "Denver", "Minneapolis", "Portland", "Baltimore", "Washington",
            "Las Vegas", "San Jose", "Orlando", "Sacramento", "Austin", "Columbus",
            "Indianapolis", "Charlotte", "Nashville", "Louisville", "Milwaukee", "Kansas City",
            "Cleveland", "Pittsburgh", "St. Louis", "Raleigh", "Tampa", "Jacksonville",
            "Memphis", "Salt Lake City", "New Orleans", "Oklahoma City", "Albuquerque",
            "Buffalo", "Cincinnati", "Omaha", "Richmond", "Hartford", "Birmingham",
            "Anchorage", "Honolulu", "Madison", "Des Moines", "Fresno", "Rochester",
            "Spokane", "Tulsa", "Boise", "Colorado Springs", "Wichita", "Tacoma",
            "Lexington", "Baton Rouge", "Aurora", "St. Paul", "Chattanooga", "Grand Rapids",
            "Knoxville", "Springfield", "Provo", "Santa Fe", "Sioux Falls", "Wilmington",
            "Fort Wayne", "Dayton", "Lincoln", "Lansing", "Mobile", "Durham", "Augusta",
            "Little Rock", "Oceanside", "Savannah", "Madison", "Boulder", "Sioux City",
            "Santa Barbara", "Salem", "Eugene", "Worcester", "Toledo", "Huntsville",
            "Santa Clara", "Santa Monica", "Naples", "Bismarck", "Billings", "Fargo",
            "Cheyenne", "Rapid City", "Flagstaff"]


def offset_weather(): #pagination #avoid duplicates
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM weather")
    offset = cur.fetchone()[0]
    conn.close()
    return offset

conn = sqlite3.connect("project.db")
cur = conn.cursor()
cur.execute("SELECT id, name FROM cities WHERE id NOT IN (SELECT city_id FROM weather)")
listed_cities = [row[0] for row in cur.fetchall()]

cities_list = []
for city in city_bank:
    if city not in listed_cities:
        cities_list.append(city)
    if len(cities_list)>= limit:
        break

for city_name in cities_list:
    base = "https://api.openweathermap.org/data/2.5/weather"
    params = {
            "appid": open_weather_api,
            "q": city,
            "units": "metric",
            "offset": offset_weather(),
            "limit": limit
        }
    response = requests.get(base, params=params)
    info = response.json()

    if "weather" not in info:
        continue

    cur.execute("INSERT OR IGNORE INTO cities (name) VALUES (?)", (city_name,))
    cur.execute("SELECT id FROM cities WHERE name=?", (city_name,))
    city_id = cur.fetchone()[0]

    cur.execute("""
    INSERT OR IGNORE INTO weather
    (city_id, main_group, weather_des)
    VALUES (?, ?, ?)""", (city_id, info["weather"][0]["main"], info["weather"][0]["description"]))

conn.commit()
cur.execute("SELECT COUNT(*) FROM cities")
print(cur.fetchone()[0])
conn.close()
print("Data from OpenWeather has been stored.")



        # skip if a city is not found
        #if info.get("cod") != 200:
       #     print("Error for", city, "->", info.get("message"))
        #    continue

