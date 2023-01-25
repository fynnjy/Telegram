import json


def user_text_saver(message):
    user_message = {
        "text": message
    }

    with open("UserTexts/text.json", "w", encoding="utf-8") as file:
        json.dump(user_message, file, indent=4, ensure_ascii=False)
