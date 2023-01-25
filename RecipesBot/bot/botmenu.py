import sqlite3


# Function for selecting a dish from the database
def choice_of_dish(name):
    # Connect DB and create new table
    connect = sqlite3.connect('../db/info.db')
    cursor = connect.cursor()

    input_title = name.lower()
    dishes = []
    for values in cursor.execute(f"SELECT * FROM recipes"):
        title = values[1]
        image = f"E:/Python/TeleBots/RecipesBot/panel/{values[2]}"
        description = values[3]

        dish = {
            'title': title,
            'image': image,
            'description': description
        }

        if input_title in dish['title'].lower():
            dishes.append(dish)
        else:
            pass

    connect.close()
    return dishes
