import matplotlib.pyplot as plt
import sqlite3

def create_bar_chart(database, cuisines):
    # bar chart of the number of recipes from a cuisine
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    placeholders = ', '.join(['?'] * len(cuisines))
    
    query_ids = f"""
    SELECT id, name 
    FROM cuisines 
    WHERE name IN ({placeholders})
    """

    cursor.execute(query_ids, cuisines)
    id_results = cursor.fetchall()

    if not id_results:
        print(f"No cuisines found matching: {cuisines}")
        conn.close()
        return

    cuisine_ids = []
    cuisine_names = []

    for ids, names in id_results:
        cuisine_ids.append(ids)
        cuisine_names.append(names)

    id_placeholders = ', '.join(['?'] * len(cuisine_ids))

    query = f"""
    SELECT r.cuisine_id, c.name, COUNT(*) as recipe_count 
    FROM recipes r
    JOIN cuisines c ON r.cuisine_id = c.id
    WHERE r.cuisine_id IN ({id_placeholders})
    GROUP BY r.cuisine_id, c.name
    ORDER BY recipe_count DESC
    """

    cursor.execute(query, cuisine_ids)
    results = cursor.fetchall()
    conn.close()

    #load data
    cuisines_list = []
    counts = []

    for cuisine_id, cuisine_name, count in results:
        cuisines_list.append(cuisine_name)
        counts.append(count)

    #bar

    color_palette = [
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
        '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    ]

    bars = plt.bar(cuisines_list, counts, color=color_palette[:len(cuisines_list)])

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
    
    cursor.execute("SELECT id FROM cities WHERE name = ?", (city,))
    city_result = cursor.fetchone()

    city_id = city_result[0]

    if not city_result:
        print(f"City '{city}' not found in database")

    query = """
    SELECT r.name, r.latitude, r.longitude, c.name as cuisine_name 
    FROM restaurants r
    LEFT JOIN cuisines c ON r.cuisine_id = c.id 
    WHERE r.city_id = ?
    """
    
    cursor.execute(query, (city_id,))
    results = cursor.fetchall()
    
    conn.close()
    
    if not results:
        print(f"No restaurants found in {city}")
        return
    
    #load data
    names = []
    lats = []
    lons = []
    cuisines = []

    for name, lat, lon, cuisine in results:
        names.append(name)
        lats.append(lat)
        lons.append(lon)
        cuisines.append(cuisine)
    
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
    SELECT w.main_group, COUNT(DISTINCT w.city_id) as city_count 
    FROM Weather w
    GROUP BY w.main_group 
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

show_all_charts("project.db", ["Indian", "Mexican", "Chinese"], "Detroit")