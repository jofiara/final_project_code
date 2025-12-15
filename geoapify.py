import requests
import sqlite3
from api_key import geoapify_api_places


new_restaurants = 0
limit = 25

city_locations = [
    ("Detroit", 42.3314, -83.0458),
    ("Chicago", 41.8781, -87.6298),
    ("New York", 40.7128, -74.0060),
    ("Los Angeles", 34.0522, -118.2437),
    ("Houston", 29.7604, -95.3698),
    ("Seattle", 47.6062, -122.3321),
    ("Miami", 25.7617, -80.1918),
    ("Denver", 39.7392, -104.9903),
    ("Minneapolis", 44.9778, -93.2650),
    ("Portland", 45.5152, -122.6784),
    ("Baltimore", 39.2904, -76.6122),
    ("Washington", 38.9072, -77.0369),
    ("Las Vegas", 36.1699, -115.1398),
    ("San Jose", 37.3382, -121.8863),
    ("Orlando", 28.5383, -81.3792),
    ("Sacramento", 38.5816, -121.4944),
    ("Austin", 30.2672, -97.7431),
    ("Columbus", 39.9612, -82.9988),
    ("Indianapolis", 39.7684, -86.1581),
    ("Charlotte", 35.2271, -80.8431),
    ("Nashville", 36.1627, -86.7816),
    ("Louisville", 38.2527, -85.7585),
    ("Milwaukee", 43.0389, -87.9065),
    ("Kansas City", 39.0997, -94.5786),
    ("Cleveland", 41.4993, -81.6944),
    ("Pittsburgh", 40.4406, -79.9959),
    ("St. Louis", 38.6270, -90.1994),
    ("Raleigh", 35.7796, -78.6382),
    ("Tampa", 27.9506, -82.4572),
    ("Jacksonville", 30.3322, -81.6557),
    ("Memphis", 35.1495, -90.0490),
    ("Salt Lake City", 40.7608, -111.8910),
    ("New Orleans", 29.9511, -90.0715),
    ("Oklahoma City", 35.4676, -97.5164),
    ("Albuquerque", 35.0844, -106.6504),
    ("Buffalo", 42.8864, -78.8784),
    ("Cincinnati", 39.1031, -84.5120),
    ("Omaha", 41.2565, -95.9345),
    ("Richmond", 37.5407, -77.4360),
    ("Hartford", 41.7658, -72.6734),
    ("Birmingham", 33.5186, -86.8104),
    ("Anchorage", 61.2181, -149.9003),
    ("Honolulu", 21.3069, -157.8583),
    ("Madison", 43.0731, -89.4012),
    ("Des Moines", 41.5868, -93.6250),
    ("Fresno", 36.7378, -119.7871),
    ("Rochester", 43.1566, -77.6088),
    ("Spokane", 47.6588, -117.4260),
    ("Tulsa", 36.1539, -95.9928),
    ("Boise", 43.6150, -116.2023),
    ("Colorado Springs", 38.8339, -104.8214),
    ("Wichita", 37.6872, -97.3301),
    ("Tacoma", 47.2529, -122.4443),
    ("Lexington", 38.0406, -84.5037),
    ("Baton Rouge", 30.4515, -91.1871),
    ("Aurora", 39.7294, -104.8319),
    ("St. Paul", 44.9537, -93.0900),
    ("Chattanooga", 35.0456, -85.3097),
    ("Grand Rapids", 42.9634, -85.6681),
    ("Knoxville", 35.9606, -83.9207),
    ("Springfield", 39.7817, -89.6501),
    ("Provo", 40.2338, -111.6585),
    ("Santa Fe", 35.6870, -105.9378),
    ("Sioux Falls", 43.5460, -96.7311),
    ("Wilmington", 34.2257, -77.9447),
    ("Fort Wayne", 41.0793, -85.1394),
    ("Dayton", 39.7589, -84.1916),
    ("Lincoln", 40.8136, -96.7026),
    ("Lansing", 42.7325, -84.5555),
    ("Mobile", 30.6954, -88.0399),
    ("Durham", 35.9940, -78.8986),
    ("Augusta", 33.4735, -82.0105),
    ("Little Rock", 34.7465, -92.2896),
    ("Oceanside", 33.1959, -117.3795),
    ("Savannah", 32.0809, -81.0912),
    ("Boulder", 40.01499, -105.2705),
    ("Sioux City", 42.4998, -96.4003),
    ("Santa Barbara", 34.4208, -119.6982),
    ("Salem", 44.9429, -123.0351),
    ("Eugene", 44.0521, -123.0868),
    ("Worcester", 42.2626, -71.8023),
    ("Toledo", 41.6528, -83.5379),
    ("Huntsville", 34.7304, -86.5861),
    ("Santa Clara", 37.3541, -121.9552),
    ("Santa Monica", 34.0195, -118.4912),
    ("Naples", 26.1420, -81.7948),
    ("Bismarck", 46.8083, -100.7837),
    ("Billings", 45.7833, -108.5007),
    ("Fargo", 46.8772, -96.7898),
    ("Cheyenne", 41.1400, -104.8202),
    ("Rapid City", 44.0805, -103.2310),
    ("Flagstaff", 35.1983, -111.6513),
    ("Philadelphia", 39.9526, -75.1652),
    ("Phoenix", 33.4484, -112.0740),
    ("San Antonio", 29.4241, -98.4936),
    ("San Diego", 32.7157, -117.1611),
    ("Dallas", 32.7767, -96.7970),
    ("El Paso", 31.7771, -106.4870),
    ("Tucson", 32.2226, -110.9747),
    ("Mesa", 33.4152, -111.8315),
    ("Atlanta", 33.7490, -84.3880),
    ("Boston", 42.3601, -71.0589),
    ("Providence", 41.8239, -71.4128),
    ("Reno", 39.5296, -119.8138),
    ("Albany", 42.6526, -73.7562),
    ("Montgomery", 32.3792, -86.3077),
    ("Columbia", 34.0007, -81.0348)
]
#need to fix this
def offset_cities(): #pagination #avoid duplicates
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(DISTINCT city_id) FROM restaurants")
    offset = cur.fetchone()[0]
    conn.close()
    return offset
def get_cuisine(cur, cuisine): #add into cuisine table
    cur.execute("INSERT OR IGNORE INTO cuisines (name) VALUES (?)", (cuisine,))
    cur.execute("SELECT id FROM cuisines WHERE name=?", (cuisine,))
    c_result = cur.fetchone()[0]
    return c_result

begin = offset_cities()

cities = city_locations[begin:begin+limit]

conn = sqlite3.connect("project.db")
cur = conn.cursor()

for city_name, lat, lon in cities:

    cur.execute("INSERT OR IGNORE INTO cities (name) VALUES (?)", (city_name,))
    cur.execute("SELECT id FROM cities WHERE name=?", (city_name,))
    city_id = cur.fetchone()[0]

    base = 'https://api.geoapify.com/v2/places?'
    params = {
        "categories": "catering.restaurant",
        "filter":f"circle:{lon},{lat},50000", #ann arbor latitude and longitude
        "offset": 0,
        "apiKey": geoapify_api_places,
        "limit": 1
    }
    response = requests.get(base, params=params)
    info = response.json()
    places = info.get('features', [])

    for place in places:
        if new_restaurants>=limit:
              break
        properties = place["properties"]
        cuisine_name = properties.get("cuisine", "Unknown").split(",")[0]
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
cur.execute("SELECT COUNT(*) FROM cities")
print(cur.fetchone()[0])
conn.close()
print("Data from Geoapify has been stored.")
