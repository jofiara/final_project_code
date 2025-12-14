import sqlite3

conn = sqlite3.connect("project.db")
cur = conn.cursor()

#recipes, cuisines
print("\nNumber of Recipes by Cuisine\n")
for row in cur.execute("""
SELECT cuisines.name, COUNT(*) as recipe_count
FROM recipes
JOIN cuisines ON recipes.cuisine_id = cuisines.id
GROUP by cuisines.name"""):
    print(row)


print("\nMost Common Ingredients by Cuisine\n")
cur.execute("""
SELECT cui.name AS cuisine,
       ing.name AS ingredient,
       COUNT(*) as ing_count
FROM recipe_ingredients ri
JOIN ingredients ing ON ri.ingredient_id = ing.id
JOIN recipes r ON ri.recipe_id = r.id
JOIN cuisines cui ON r.cuisine_id = cui.id
GROUP BY cui.name, ing.name
ORDER BY cui.name, ing_count DESC""")
    #print(row)


#might have to change, add extra calcuation?
#recipe_ingredients, cuisines
top_ingredients = {}
for cuisine, ingredient, count in cur.fetchall():
    if cuisine not in top_ingredients:
        top_ingredients[cuisine] = []
    if len(top_ingredients[cuisine])<5:
        top_ingredients[cuisine].append((ingredient, count))

for cuisine in top_ingredients:
    print(f"\n{cuisine}\n")
    for ing, count in top_ingredients[cuisine]:
        print(f"{ing}: {count}")

#restaurant #cities #weather
print("\nRestaurants by Weather Conditions")
cur.execute("""
SELECT wea.main_group, COUNT(*) AS rest_count
FROM restaurants rest
JOIN cities ci ON rest.city_id = ci.id
JOIN weather wea ON ci.id = wea.city_id
GROUP BY wea.main_group
ORDER BY rest_count DESC""")
for row in cur.fetchall():
    print(row)