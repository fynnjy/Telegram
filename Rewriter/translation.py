from googletrans import Translator
import write_or_file
import json


def translation_process(final_lang):
    with open("UserTexts/text.json", "r", encoding="utf-8") as file:
        main_text = json.load(file)

    transformation = Translator()

    if len(main_text["text"]) >= 4000:
        main_text["text"] = main_text["text"][0:3999]

    out_1 = transformation.translate(main_text["text"], dest="pl")
    out_2 = transformation.translate(out_1.text, dest="da")
    out_3 = transformation.translate(out_2.text, dest="nl")
    out_4 = transformation.translate(out_3.text, dest="fr")
    out_5 = transformation.translate(out_4.text, dest="de")
    out_6 = transformation.translate(out_5.text, dest="ga")
    out_7 = transformation.translate(out_6.text, dest="it")
    out_8 = transformation.translate(out_7.text, dest="ko")
    out_9 = transformation.translate(out_8.text, dest="tr")
    out_10 = transformation.translate(out_9.text, dest=final_lang)

    if write_or_file.check_status() == "text":
        return out_10.text

    elif write_or_file.check_status() == "file":
        with open("UserTexts/rewrote.txt", "w", encoding="utf-8") as file:
            file.write(out_10.text)

    else:
        return "Something went wrong"
