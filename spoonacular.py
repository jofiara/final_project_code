import requests
import sqlite3
from api_key import spoonacular_api


limit = 25

def offset_recipes(): #pagination #avoid duplicates
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM recipes")
    offset = cur.fetchone()[0]
    conn.close()
    return offset
    
def get_cuisine(cur, cuisine): #add into cuisine table
    cur.execute("INSERT OR IGNORE INTO cuisines (name) VALUES (?)", (cuisine,))
    cur.execute("SELECT id FROM cuisines WHERE name=?", (cuisine,))
    c_result = cur.fetchone()[0]
    return c_result


def get_ingredient(cur, name): #add into ingredient table
    cur.execute("INSERT OR IGNORE INTO ingredients (name) VALUES (?)", (name,))
    cur.execute("SELECT id FROM ingredients WHERE name=?", (name,))
    i_result = cur.fetchone()[0]
    return i_result

def recipe_ingredients(recipe_id):
    base = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": spoonacular_api}
    response = requests.get(base, params=params)
    info = response.json()
    return info.get("extendedIngredients", [])


offset = offset_recipes()


base = "https://api.spoonacular.com/recipes/complexSearch"
params = {
        "apiKey": spoonacular_api, 
        "number": limit,
        "offset": offset,
        "addRecipeInformation": True
        }
    

response = requests.get(base, params=params)
info = response.json()

conn = sqlite3.connect("project.db")
cur = conn.cursor()

results = info.get('results', [])

for recipe in results:
    cuisine = recipe["cuisines"][0] if recipe["cuisines"] else "Unknown"
    cuisine_id = get_cuisine(cur, cuisine)
    cur.execute("""
        INSERT OR IGNORE INTO recipes
        (spoon_id, title, cuisine_id, ready_time, source) VALUES (?, ?, ?, ?, ?)"""
        , (recipe["id"], recipe["title"], cuisine_id, recipe["readyInMinutes"], recipe["sourceUrl"]))
    cur.execute("SELECT id FROM recipes WHERE spoon_id=?", (recipe["id"],))
    recipe_id = cur.fetchone()[0]

    ext_ingredients = recipe_ingredients(recipe["id"]) #handle if field does not exist
    for ing in ext_ingredients:
        name = ing.get("name", "Unknown")
        ing_id = get_ingredient(cur, name)
        cur.execute("INSERT OR IGNORE INTO recipe_ingredients VALUES (?, ?)", (recipe_id, ing_id))
#fix 25 limit for ingredients
conn.commit()
conn.close()
print("Data from Spoonacular has been stored.") #confirm everything ran

