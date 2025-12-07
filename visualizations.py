import matplotlib.pyplot as plt
import sqlite3

def create_bar_chart(database, cuisines):
    # bar chart of the number of recipes from a cuisine
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    placeholders = ', '.join(['?'] * len(cuisines))
    
    query = f"""
    SELECT cuisine, COUNT(*) as recipe_count 
    FROM Recipes 
    WHERE cuisine IN ({placeholders})
    GROUP BY cuisine 
    ORDER BY recipe_count DESC
    """

    cursor.execute(query, cuisines)
    results = cursor.fetchall()
    conn.close()

    #load data
    cuisines_list = []
    counts = []

    for cuisine, count in results:
        cuisines_list.append(cuisine)
        counts.append(count)

    #bar

    bars = plt.bar(cuisines_list, counts, color='skyblue')

    plt.title('Number of Recipes per Cuisine', fontsize=13, fontfamily='Times New Roman')
    plt.xlabel('Cuisine Type', fontsize=11, fontfamily='Times New Roman')
    plt.ylabel('Number of Recipes', fontsize=11, fontfamily='Times New Roman')

    plt.xticks(fontsize=9, fontfamily='Times New Roman')
    plt.yticks(fontsize=9, fontfamily='Times New Roman')

    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, str(count), ha='center', va='bottom', fontsize= 9, fontfamily='Times New Roman')
    


def create_scatter(database, city):
    # scatter of restutrant locations in a city
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = """
    SELECT name, latitude, longitude 
    FROM Restaurants 
    WHERE city = ?
    """
    
    cursor.execute(query, (city,))
    results = cursor.fetchall()
    
    conn.close()
    
    if not results:
        print(f"No restaurants found in {city}")
        return
    
    #load data
    names = []
    lats = []
    lons = []

    for name, lat, lon in results:
        names.append(name)
        lats.append(lat)
        lons.append(lon)
    
    #scatter
    plt.scatter(lons, lats, color='gray', s=30)
    plt.title(f'Restaurants in {city}', fontsize= 13, fontfamily='Times New Roman')
    plt.xlabel('Longitude', fontsize=11, fontfamily='Times New Roman')
    plt.ylabel('Latitude', fontsize=11, fontfamily='Times New Roman')

    plt.xticks(fontsize=9, fontfamily='Times New Roman')
    plt.yticks(fontsize=9, fontfamily='Times New Roman')

    plt.grid(True)
    
    for name, lon, lat in zip(names, lons, lats):
        plt.text(lon, lat, name, fontsize=9, fontfamily='Times New Roman')
    

def create_pie_chart(database):
    # weather condition across the city
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = """
    SELECT main_group, COUNT(DISTINCT city) as city_count 
    FROM Weather 
    GROUP BY main_group 
    ORDER BY city_count DESC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print("No weather data found")
        return
    
    #load data
    conditions = []
    counts = []

    for condition, count in results:
        conditions.append(condition)
        counts.append(count)
    
    #pie
    weather_colors = {
        'Clear': 'lightyellow',
        'Clouds': 'lightgray',
        'Rain': 'lightblue',
        'Snow': 'white',
        'Thunderstorm': 'slategray',
        'Drizzle': 'skyblue',
        'Mist': 'silver',
        'Fog': 'darkgray'
    }
    
    colors = []
    for condition in conditions:
        color = weather_colors.get(condition, 'lightgreen')
        colors.append(color)
    

    plt.pie(counts, labels=conditions, colors=colors, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black', 'linewidth': 0.2}, textprops={'fontfamily': 'Times New Roman'})
    plt.title('Distribution of Weather Conditions Across Cities', fontsize=12, fontfamily='Times New Roman')
    


def show_all_charts(database, cuisines, city):
    # database = db file str, list of cuisines, city str

    plt.figure(figsize=(15, 5))
    
    # First chart
    plt.subplot(1, 3, 1)
    create_bar_chart(database, cuisines)
    
    # Second chart  
    plt.subplot(1, 3, 2)
    create_scatter(database, city)

    # Third chart
    plt.subplot(1, 3, 3)
    create_pie_chart(database)
    
    plt.tight_layout()
    plt.show()

show_all_charts()