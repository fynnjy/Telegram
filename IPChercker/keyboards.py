from aiogram.types import ReplyKeyboardMarkup

# --Main Menu--
main_menu_buttons = ["Дізнатися за IP 💻", "Створити лінк ⚡"]
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*main_menu_buttons)

# --OK/NO Menu--
okno_menu_buttons = ['Надіслати ✅', 'Скасувати 🚫']
okno_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*okno_menu_buttons)
