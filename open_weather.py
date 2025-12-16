import requests
import sqlite3
from api_key import open_weather_api

limit = 25

conn = sqlite3.connect("project.db")
cur = conn.cursor()

cur.execute("""
SELECT DISTINCT c.id, c.name
FROM restaurants r
JOIN cities c ON r.city_id = c.id
LEFT JOIN weather w ON c.id = w.city_id
WHERE w.city_id IS NULL
ORDER BY c.id
LIMIT ?
""", (limit,))

cities_list = cur.fetchall()

for city_id, city_name in cities_list:
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


    cur.execute("""
    INSERT OR IGNORE INTO weather
    (city_id, main_group, weather_des)
    VALUES (?, ?, ?)""", (city_id, info["weather"][0]["main"], info["weather"][0]["description"]))

conn.commit()
cur.execute("SELECT COUNT(*) FROM weather")
print(f"{cur.fetchone()[0]} cities' weather information is in the database.")
conn.close()
print("Data from OpenWeather has been stored.")
