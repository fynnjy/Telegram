from aiogram.types import ReplyKeyboardMarkup

# --Start Menu--
start_menu_buttons = ["Enter text 🖋", "Send file ✉️"]
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*start_menu_buttons)

# --Yes or No--
accept_buttons = ["Accept ✅", "Cancel 🚫"]
accept_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*accept_buttons)
