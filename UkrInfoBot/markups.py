from aiogram.types import ReplyKeyboardMarkup

# --Main Menu--
main_menu_buttons = ["Новини 🔖", "Погода 💧", "Валюти 💰", "Інші ресурси ⤵"]
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*main_menu_buttons)


# --Second Menu--
second_menu_buttons = ["Назад ⬅", "RBC🗞", "BBC🗞"]
second_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*second_menu_buttons)

# --OK/NO Menu--
okno_menu_buttons = ['Надіслати ✅', 'Скасувати 🚫']
okno_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*okno_menu_buttons)
