from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

accept_input = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Enter text 🖋", callback_data="enter_text"),
            InlineKeyboardButton(text="Send file ✉️", callback_data="cancel_input"),
        ],
    ]
)

text_translation = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ukrainian 🇺🇦", callback_data="to_ua"),
        ],
        [
            InlineKeyboardButton(text="English 🇬🇧", callback_data="to_en"),
        ],
        [
            InlineKeyboardButton(text="French 🇫🇷", callback_data="to_fr"),
        ],
        [
            InlineKeyboardButton(text="Polish 🇵🇱", callback_data="to_pl"),
        ],
        [
            InlineKeyboardButton(text="German 🇩🇪", callback_data="to_de"),
        ],
    ]
)
