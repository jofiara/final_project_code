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
    


def create_horizontal_bar(cuisine_name, database, num = 10):

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query = """
    SELECT i.name, COUNT(*) as count
    FROM ingredients i
    JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
    JOIN recipes r ON ri.recipe_id = r.id
    JOIN cuisines c ON r.cuisine_id = c.id
    WHERE c.name = ?
    GROUP BY i.name
    ORDER BY count DESC
    LIMIT ?
    """

    cursor.execute(query, (cuisine_name, num))
    result = cursor.fetchall()
    
    conn.close()

    if not result:
        print(f"No data found for cuisine: {cuisine_name}")
        return

    ingredients = []
    counts = []
    
    for ingredient_name, count in result:
        ingredients.append(ingredient_name)
        counts.append(count)

    ingredients.reverse()
    counts.reverse()

    color_palette = [
        '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    ]

    colors = color_palette[:len(ingredients)]
    colors.reverse()
    
    y_pos = range(len(ingredients))
    bars = plt.barh(y_pos, counts, color=colors, height=0.7)

    plt.yticks(y_pos, ingredients, fontsize=10, fontfamily='Times New Roman')
    plt.xlabel('Number of Recipes Using Ingredient', fontsize=11, fontfamily='Times New Roman')
    plt.title(f'Top {num} Ingredients in {cuisine_name} Cuisine', fontsize=13, fontfamily='Times New Roman')

    for i, (bar, count) in enumerate(zip(bars, counts)):
        width = bar.get_width()
        plt.text(width + max(counts)*0.01, i, str(count), 
                va='center', fontsize=9, fontfamily='Times New Roman')
    

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
        'Mist': 'lightpink',
        'Fog': 'darkgray'
    }
    
    colors = []
    for condition in conditions:
        color = weather_colors.get(condition, 'lightgreen')
        colors.append(color)
    
    wedges, texts, autotexts = plt.pie(counts, labels=conditions, colors=colors, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black', 'linewidth': 0.2}, textprops={'fontfamily': 'Times New Roman'})
        
    for autotext in autotexts:
        autotext.set_fontfamily('Times New Roman')
        autotext.set_fontsize(6)
    plt.title('Distribution of Restaurants by Weather Conditions', fontsize=12, fontfamily='Times New Roman')
    

def create_box_plot(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query = """
    SELECT c.name AS cuisine_name, r.ready_time
    FROM recipes r
    JOIN cuisines c ON r.cuisine_id = c.id
    WHERE r.ready_time IS NOT NULL
    ORDER BY c.name
    """

    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    if not result:
        print("No data found.")
        return

    cuisine_times = {}
    for cuisine, time in result:
        if cuisine not in cuisine_times:
            cuisine_times[cuisine] = []
        cuisine_times[cuisine].append(time)

    labels = list(cuisine_times.keys())
    data_lis = list(cuisine_times.values())
    plt.boxplot(data_lis, tick_labels=labels)

    plt.title('Average Cooking Time per Cuisine',fontsize=12, fontfamily='Times New Roman')
    plt.xlabel('Cuisine',fontsize=11, fontfamily='Times New Roman')
    plt.ylabel('Ready Time (minutes)',fontsize=11, fontfamily='Times New Roman')
    plt.xticks(rotation=45, ha='right', fontsize=9, fontfamily='Times New Roman')
    plt.yticks(fontsize=9, fontfamily='Times New Roman')

    plt.grid(True, alpha=0.3)
    plt.ylim(0, 200)


def show_all_charts(database, cuisines):
    # database = db file str, list of cuisines, city str

    plt.figure(figsize=(15, 10))
    
    # First chart
    plt.subplot(2, 2, 1)
    create_bar_chart(database, cuisines[1::])
    
    # Second chart  
    plt.subplot(2, 2, 2)
    create_horizontal_bar(cuisines[0], database)

    # Third chart
    plt.subplot(2, 2, 3)
    create_pie_chart(database)

    # Fourth chart
    plt.subplot(2, 2, 4)
    create_box_plot(database)
    
    plt.tight_layout()
    plt.show()

show_all_charts("project.db", ["Unknown", "Mexican", "Chinese", "Mediterranean"])