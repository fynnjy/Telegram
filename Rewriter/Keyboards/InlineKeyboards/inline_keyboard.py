from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

accept_input = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Enter text π", callback_data="enter_text"),
            InlineKeyboardButton(text="Send file βοΈ", callback_data="cancel_input"),
        ],
    ]
)

text_translation = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ukrainian πΊπ¦", callback_data="to_ua"),
        ],
        [
            InlineKeyboardButton(text="English π¬π§", callback_data="to_en"),
        ],
        [
            InlineKeyboardButton(text="French π«π·", callback_data="to_fr"),
        ],
        [
            InlineKeyboardButton(text="Polish π΅π±", callback_data="to_pl"),
        ],
        [
            InlineKeyboardButton(text="German π©πͺ", callback_data="to_de"),
        ],
    ]
)
