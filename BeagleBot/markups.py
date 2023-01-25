from aiogram.types import ReplyKeyboardMarkup

# --Start Menu--
start_menu_buttons = ["Social networks ☑", "Clear lists 🗑"]
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*start_menu_buttons)

# --Main Menu--
main_menu_buttons = ["Instagram 💜", "Youtube ❤", "TikTok 🖤", "Back ⬅"]
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*main_menu_buttons)

# --For Delete--
delete_buttons = ["Instagram 🗒", "Youtube 🗒", "TikTok 🗒", "Back ⬅"]
delete_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*delete_buttons)

# --Social Networks Menu--
social_networks_buttons = ["Back ⬅", "Add ➕", "Delete ➖", 'Check existing 🗒']
social_networks_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*social_networks_buttons)

# --Yes or No--
accept_buttons = ["Accept ✅", "Cancel 🚫"]
accept_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*accept_buttons)
