import requests
import sqlite3
from api_key import open_weather_api

limit = 25

conn = sqlite3.connect("project.db")
cur = conn.cursor()

cur.execute("""
SELECT DISTINCT c.name
FROM restaurants r
JOIN cities c ON r.city_id = c.id""")
rest_cities = [row[0] for row in cur.fetchall()]

cities_list = []
for city in rest_cities:
    if city not in cities_list:
        cities_list.append(city)
    if len(cities_list)>= limit:
        break

for city_name in cities_list:
    base = "https://api.openweathermap.org/data/2.5/weather"
    params = {
            "appid": open_weather_api,
            "q": city_name,
            "units": "metric",
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
