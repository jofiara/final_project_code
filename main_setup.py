import sqlite3

def setup_database():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()

    # for recipies table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Recipes (
        id INTEGER PRIMARY KEY,
        recipe_id INTEGER UNIQUE,
        title TEXT,
        cuisine TEXT,
        ready_time INTEGER
    );
    """)

    # for ingredients table 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Ingredients (
        id INTEGER PRIMARY KEY,
        recipe_id INTEGER,
        ingredient_name TEXT
    );
    """)

    # for restaurants table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Restaurants (
        id INTEGER PRIMARY KEY,
        place_id TEXT UNIQUE,
        name TEXT,
        city TEXT,
        cuisine TEXT,
        latitude REAL,
        longitude REAL,
        distance REAL
    );
    """)

    # weather
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Weather (
        id INTEGER PRIMARY KEY,
        city TEXT,
        main_group TEXT
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("Database created!")