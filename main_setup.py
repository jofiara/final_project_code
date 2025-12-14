import sqlite3

def setup_database():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()

    #cuisines table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cuisines (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    );
    """)

    # for recipies table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        spoon_id INTEGER UNIQUE,
        title TEXT,
        cuisine_id INTEGER,
        ready_time INTEGER,
        source TEXT
    );
    """)

    # for ingredients table 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    );
    """)

    #specific ingredient relationships
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recipe_ingredients (
        recipe_id INTEGER,
        ingredient_id INTEGER,
        UNIQUE(recipe_id, ingredient_id)
    );
    """)

    # for restaurants table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY,
        geoapify_id TEXT UNIQUE,
        name TEXT,
        city_id INTEGER,
        cuisine_id INTEGER,
        latitude REAL,
        longitude REAL,
        distance REAL
    );
    """)

    # weather - might remove last line
    cur.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY,
        city_id INTEGER UNIQUE,
        main_group TEXT,
        weather_des TEXT 
    );
    """)

    #cities
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE 
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("Database created!")