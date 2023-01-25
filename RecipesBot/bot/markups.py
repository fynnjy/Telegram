from telebot import types
import sqlite3

# Main Menu Keyboard
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
about_button = types.KeyboardButton("Про мене 📰")
recipes_button = types.KeyboardButton("Рецепти 👩‍🍳")

main_keyboard.add(about_button,
                  recipes_button)

# Gender Keyboard
gender_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
male_button = types.KeyboardButton("Чоловік 🤵‍♂")
female_button = types.KeyboardButton("Жінка 👩‍🦱")

gender_keyboard.add(male_button,
                    female_button)


# Function to get the name for the future buttons of the keyboard with recipes
def recipes_titles_func():
    # Connect DB and create new table
    connect = sqlite3.connect('../db/info.db')
    cursor = connect.cursor()

    titles = []
    for values in cursor.execute(f"SELECT * FROM recipes"):
        titles.append(values[1])

    connect.close()
    return titles


# Function for keyboard output with recipes
def recipes_keyboard_func():
    # Recipes Keyboard
    recipes_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton("Назад ↩")

    return recipes_keyboard.add(*recipes_titles_func(), back_button)

