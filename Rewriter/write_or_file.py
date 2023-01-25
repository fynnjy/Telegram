import json


def variant(status):
    current_method = {
        "status": status
    }

    with open("UserTexts/status.json", "w", encoding="utf-8") as file:
        json.dump(current_method, file, indent=4, ensure_ascii=False)


def check_status():
    with open("UserTexts/status.json", "r", encoding="utf-8") as file:
        status = json.load(file)

    for k, v in status.items():
        return v
