from telebot import custom_filters
from datetime import date
from telebot import types
from time import sleep
import verification
import telebot
import markups
import botmenu
import config
import texts
import fsm


# Passing the storage to a bot
bot = telebot.TeleBot(config.TOKEN)


# After sending the start command
@bot.message_handler(commands=['start'], state=None)
def start_command(message):

    """Checks the user for existence in the database.
    Transition if the user is new, output the questionnaire if the user exists"""
    check_info = verification.check_user(message.from_user.id)

    # Creating a table with recipes in case of its absence
    verification.db_recipes_creation()

    if not check_info:
        bot.send_sticker(message.chat.id, texts.hello_sticker,
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id,
                         f"Вітаю, <b>{message.from_user.username}</b>!\n"
                         f"{texts.hello_message}",
                         parse_mode='html')

        sleep(0.5)
        bot.send_message(message.chat.id, texts.name_question)
        bot.set_state(message.from_user.id, fsm.AboutUser.name, message.chat.id)

    else:
        bot.send_sticker(message.chat.id, texts.back_sticker)
        bot.send_message(message.chat.id,
                         f"<b>{check_info['input_name']}</b>, "
                         f"ви вже зареєстровані 🙋",
                         reply_markup=markups.main_keyboard, parse_mode='html')

        old_user = verification.check_user(message.from_user.id)
        user_info = ("🔻 <u>Ваша анкета</u> 🔻\n\n"
                     f"<b>Ім'я:</b> {old_user['input_name']}\n"
                     f"<b>Стать:</b> {old_user['gender']}\n"
                     f"<b>Дата реєстрації:</b> {old_user['registration_period']}\n")

        bot.send_message(message.chat.id, user_info,
                         reply_markup=markups.main_keyboard,
                         parse_mode='html')


# State getting the user's name
@bot.message_handler(state=fsm.AboutUser.name, is_digit=False)
def user_name(message):

    """A state that receives the user's name and records it.
    Does not work if the username consists only of numbers."""

    bot.send_message(message.chat.id, f"Приємно познайомитись, {message.text} 🙋")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text

    sleep(0.5)
    bot.send_message(message.chat.id, texts.gender_question,
                     reply_markup=markups.gender_keyboard)
    bot.set_state(message.from_user.id, fsm.AboutUser.gender, message.chat.id)


# Error of getting the user's name
@bot.message_handler(state=fsm.AboutUser.name, is_digit=True)
def user_name(message):

    """The function responsible for the refusal of reception,
    in case the user has entered only digits in the name field."""

    sleep(0.5)
    bot.send_message(message.chat.id, texts.name_input_error)


# State getting the user's gender
@bot.message_handler(state=fsm.AboutUser.gender)
def user_name(message):

    """Switching to the second state to
    receive the user's gender after entering from the buttons."""

    sleep(0.5)
    bot.send_message(message.chat.id, texts.successful_registration,
                     reply_markup=markups.main_keyboard)

    registration_date = str(date.today())

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        # Calling the function to fill in user data
        verification.registration(message.from_user.id,
                                  message.from_user.username,
                                  data['name'],
                                  message.text[:-3],
                                  message.from_user.first_name,
                                  message.from_user.last_name,
                                  registration_date)

    bot.delete_state(message.from_user.id, message.chat.id)


# Switching between keyboards and echo reply
@bot.message_handler(content_types=['text'])
def echo_answer(message):

    """The handler is responsible for processing queries and displaying recipes,
    moving to the main menu and displaying information about the user."""

    if message.text == "Про мене 📰":
        old_user = verification.check_user(message.from_user.id)
        user_info = ("🔻 <u>Ваша анкета</u> 🔻\n\n"
                     f"<b>Ім'я:</b> {old_user['input_name']}\n"
                     f"<b>Стать:</b> {old_user['gender']}\n"
                     f"<b>Дата реєстрації:</b> {old_user['registration_period']}\n")

        sleep(0.5)
        bot.send_message(message.chat.id, user_info,
                         reply_markup=markups.main_keyboard,
                         parse_mode='html')

    elif message.text == "Рецепти 👩‍🍳":
        bot.send_message(message.chat.id, texts.recipes_menu_message,
                         reply_markup=markups.recipes_keyboard_func())

    elif message.text in markups.recipes_titles_func():
        appeal_to_db = botmenu.choice_of_dish(message.text)

        for item in appeal_to_db:
            image = open(item['image'], 'rb')
            dish = f'<b>{item["title"]}</b>\n\n' \
                   f'<i>{item["description"]}</i>'

            bot.send_photo(message.chat.id, image)
            bot.send_message(message.chat.id, dish,
                             parse_mode='html')

    elif message.text == "Назад ↩":
        bot.send_message(message.chat.id, texts.back_button,
                         reply_markup=markups.main_keyboard)

    else:
        bot.send_message(message.chat.id,
                         f'<b>{texts.echo_reply}</b>',
                         parse_mode='html')


# Response to the user upon receipt photo
@bot.message_handler(content_types=['photo'])
def echo_answer(message):
    bot.send_message(message.chat.id,
                     f'<b>{texts.content_photo}</b>',
                     parse_mode='html')


# Response to the user upon receipt video
@bot.message_handler(content_types=['video'])
def echo_answer(message):
    bot.send_message(message.chat.id,
                     f'<b>{texts.content_video}</b>',
                     parse_mode='html')


# Response to the user upon receipt voice
@bot.message_handler(content_types=['voice'])
def echo_answer(message):
    bot.send_message(message.chat.id,
                     f'<b>{texts.content_voice}</b>',
                     parse_mode='html')


# Response to the user upon receipt sticker
@bot.message_handler(content_types=['sticker'])
def echo_answer(message):
    bot.send_message(message.chat.id,
                     f'<b>{texts.content_sticker}</b>',
                     parse_mode='html')


# Response to the user upon receipt document
@bot.message_handler(content_types=['document'])
def echo_answer(message):
    bot.send_message(message.chat.id,
                     f'<b>{texts.content_document}</b>',
                     parse_mode='html')


# Adding custom filters
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

# Start polling
bot.infinity_polling()
