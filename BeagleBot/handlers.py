from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from Middlewares.throttling import ThrottlingMiddleware
from Middlewares.rateLimits import rate_limit
from config import TOKEN, CHANNEL_ID

import botStates
import logging
import asyncio
import markups
import logic
import texts
import json

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


# Start function
@dp.message_handler(commands=['start'])
@rate_limit(600)  # Ability to send messages every 10 minutes
async def start_bot(message: types.Message):
    logic.new_bot_user(message.from_user.id)

    with open('Dicts/existinguser.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    status = data['status']

    if status == 'old':
        await message.answer_sticker(texts.hello_sticker)
        await message.answer(f'{texts.user_returning} '
                             f'<b>{message.from_user.username}</b> 🖖\n'
                             f'{texts.hello_message}',
                             reply_markup=markups.start_keyboard)

    else:
        await message.answer_sticker(texts.hello_sticker)
        await message.answer(f'Hi <b>{message.from_user.username}</b> 🖖\n'
                             f'{texts.hello_message}',
                             reply_markup=markups.start_keyboard)


    await asyncio.sleep(1)
    logic.keyboard_choice('start menu')


# Go to the tab for working with Instagram accounts
@dp.message_handler(Text(equals='Social networks ☑'))
@rate_limit(0.5) # Ability to send a request every 0.5 second
async def instagram_action(message: types.Message):
    await message.answer(texts.after_start_keyboard,
                         reply_markup=markups.main_keyboard)

    logic.keyboard_choice('main menu')


# Go to the tab for working with Instagram accounts
@dp.message_handler(Text(equals='Clear lists 🗑'))
@rate_limit(0.5) # Ability to send a request every 1 second
async def instagram_action(message: types.Message):
    await message.answer(texts.after_start_keyboard,
                         reply_markup=markups.delete_keyboard)

    logic.keyboard_choice('clear lists')


# Go to the tab for working with Instagram accounts
@dp.message_handler(Text(equals='Instagram 💜'))
@rate_limit(0.5) # Ability to send a request every 1 second
async def instagram_action(message: types.Message):
    await message.answer(texts.social_networks_action,
                         reply_markup=markups.social_networks_keyboard)

    logic.network_choice('instagram')
    logic.keyboard_choice('instagram buttons')


# Go to the tab for working with Youtube accounts
@dp.message_handler(Text(equals='Youtube ❤'))
@rate_limit(0.5) # Ability to send a request every 1 second
async def instagram_action(message: types.Message):
    await message.answer(texts.social_networks_action,
                         reply_markup=markups.social_networks_keyboard)

    logic.network_choice('youtube')
    logic.keyboard_choice('youtube buttons')


# Go to the tab for working with TikTok accounts
@dp.message_handler(Text(equals='TikTok 🖤'))
@rate_limit(0.5) # Ability to send a request every 1 second
async def instagram_action(message: types.Message):
    await message.answer(texts.social_networks_action,
                         reply_markup=markups.social_networks_keyboard)

    logic.network_choice('tiktok')
    logic.keyboard_choice('tiktok buttons')


# Return to the previous menu
@dp.message_handler(Text(equals='Back ⬅'))
@rate_limit(0.5) # Ability to send a request every 0.5 seconds
async def back_action(message: types.Message):
    with open('Dicts/relevant_keyboard.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    relevant_keyboard = data['relevant_keyboard']

    if relevant_keyboard == 'instagram buttons' \
            or relevant_keyboard == 'youtube buttons' \
            or relevant_keyboard == 'tiktok buttons'\
            or relevant_keyboard == 'add'\
            or relevant_keyboard == 'del':

        logic.keyboard_choice('main menu')
        await message.answer(texts.back_action_message,
                             reply_markup=markups.main_keyboard)

    else:
        await message.answer(texts.back_action_message,
                             reply_markup=markups.start_keyboard)


# Button for adding a new user to an existing list
@dp.message_handler(Text(equals='Add ➕'), state=None)
@rate_limit(0.5)# Ability to send a request every 1 second
async def add_user(message: types.Message):
    with open('Dicts/relevant_network.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    relevant_network = data['relevant_network']

    if relevant_network == 'instagram':
        await message.answer(f'Instagram - {texts.under_development}')

        logic.keyboard_choice('add')

    elif relevant_network == 'youtube':
        await message.answer(texts.after_press_add_user_button,
                                 reply_markup=types.ReplyKeyboardRemove())

        await botStates.AddUser.yt_link.set()
        logic.keyboard_choice('add')

    elif relevant_network == 'tiktok':
        await message.answer(f'TikTok - {texts.under_development}')
        logic.keyboard_choice('add')


# Button for adding a new user to an existing list
@dp.message_handler(Text(equals='Delete ➖'), state=None)
@rate_limit(0.5)# Ability to send a request every 1 second
async def add_user(message: types.Message):
    with open('Dicts/relevant_network.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    relevant_network = data['relevant_network']

    if relevant_network == 'instagram':
        await message.answer('Instagram list is empty\n'
                             f'{texts.under_development}')

    elif relevant_network == 'youtube':
        await message.answer(texts.after_press_delete_user_button,
                             reply_markup=types.ReplyKeyboardRemove())

        await botStates.DeleteUser.yt_user.set()

    elif relevant_network == 'tiktok':
        await message.answer('TikTok list is empty\n'
                             f'{texts.under_development}')

    else:
        await message.answer(texts.error_message)

    logic.keyboard_choice('del')


# Adding a YouTube user
@dp.message_handler(state=botStates.AddUser.yt_link)
async def link_taker(message: types.Message, state: FSMContext):
    user_link = message.text
    logic.create_yt_user(user_link, message.from_user.id)

    with open('Dicts/user_status.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    user_status = data['status']

    if user_status == texts.already_exists_user:
        await message.answer(f'<b>{texts.already_exists_user}</b>',
                             reply_markup=markups.social_networks_keyboard)
        logic.keyboard_choice('youtube buttons')
        await state.finish()

    elif user_status == texts.non_existent_user:
        await message.answer(f'<b>{texts.non_existent_user}</b>',
                             reply_markup=markups.social_networks_keyboard)
        logic.keyboard_choice('youtube buttons')
        await state.finish()

    elif user_status == texts.successfully_added_user:
        await message.answer(f'<b>{texts.successfully_added_user}</b>',
                             reply_markup=markups.social_networks_keyboard)
        logic.keyboard_choice('youtube buttons')
        await state.finish()

    else:
        await message.answer(f'<b>{texts.incorrect_link}</b>',
                             reply_markup=markups.social_networks_keyboard)
        logic.keyboard_choice('youtube buttons')
        await state.finish()


# Deleting a YouTube user
@dp.message_handler(state=botStates.DeleteUser.yt_user)
async def link_taker(message: types.Message, state: FSMContext):
    user_link = message.text
    logic.delete_yt_user(user_link, message.from_user.id)

    with open('Dicts/user_status.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    user_status = data['status']

    if user_status == texts.successfully_deleted_user:
        await message.answer(f'<b>{texts.successfully_deleted_user}</b>',
                             reply_markup=markups.social_networks_keyboard)
        logic.keyboard_choice('youtube buttons')
        await state.finish()

    elif user_status == texts.not_in_list:
        await message.answer(f'<b>{texts.not_in_list}</b>',
                             reply_markup=markups.social_networks_keyboard)
        logic.keyboard_choice('youtube buttons')
        await state.finish()

    elif user_status == texts.incorrect_link:
        await message.answer(f'<b>{texts.incorrect_link}</b>',
                             reply_markup=markups.social_networks_keyboard)
        logic.keyboard_choice('youtube buttons')
        await state.finish()

    else:
        await message.answer(f'<b>{texts.error_message}</b>',
                             reply_markup=markups.social_networks_keyboard)
        logic.keyboard_choice('youtube buttons')
        await state.finish()


# Display a list of users
@dp.message_handler(Text(equals='Check existing 🗒'))
@rate_limit(0.5) # Ability to send a request every 1 second
async def check_users_list(message: types.Message):
    with open('Dicts/relevant_network.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    await message.answer(f'<b>{texts.check_existing}</b>')

    relevant_network = data['relevant_network']

    if relevant_network == 'instagram':
        await message.answer('Instagram list is empty\n'
                             f'{texts.under_development}')

    elif relevant_network == 'youtube':
        logic.get_info_update_yt(message.from_user.id) # Update all dict positions info

        if logic.get_info_update_yt(message.from_user.id) == False:
            await asyncio.sleep(1)
            await message.answer(f'<b>{texts.empty_list}</b>')

        else:
            with open('Dicts/users.json', 'r', encoding='utf-8') as file:
                check_data = json.load(file)

            users_list = []
            for users in check_data['Values']:
                for k, v in users.items():
                    users_list.append(k)

            current_user = users_list.index(str(message.from_user.id))
            dict_of_current_user = check_data['Values'][current_user]

            social_networks_list = []
            for k, v in dict_of_current_user.items():
                for item in v:
                    social_networks_list.append(item)

            youtube_dict = social_networks_list[1]

            count = 1
            for k, v in youtube_dict.items():
                for info in v:
                    await message.answer(f'<b>User: №{count}</b>\n'
                                         f'<b>Channel:</b> {info["id"]}\n'
                                         f'<b>Subscribers:</b> {info["subscribers"]}\n\n'
                                         f'{hlink("Go to channel 👁", info["link"])}')
                    count += 1

    elif relevant_network == 'tiktok':
        await message.answer('TikTok list is empty\n'
                             f'{texts.under_development}')

    else:
        await message.answer(texts.error_message)


# Cleaning the list of Instagram users
@dp.message_handler(Text(equals='Instagram 🗒'))
@rate_limit(0.5) # Ability to send a request every 1 second
async def instagram_action(message: types.Message):
    await message.answer(texts.lists_deleting,
                         reply_markup=markups.accept_keyboard)

    logic.network_choice('instagram')
    await botStates.AcceptButtons.accept.set()


# Cleaning the list of Youtube users
@dp.message_handler(Text(equals='Youtube 🗒'), state=None)
@rate_limit(1) # Ability to send a request every 1 second
async def instagram_action(message: types.Message):
    await message.answer(texts.lists_deleting,
                         reply_markup=markups.accept_keyboard)

    logic.network_choice('youtube')
    await botStates.AcceptButtons.accept.set()


# Cleaning the list of TikTok users
@dp.message_handler(Text(equals='TikTok 🗒'))
@rate_limit(1) # Ability to send a request every 1 second
async def instagram_action(message: types.Message):
    await message.answer(texts.lists_deleting,
                         reply_markup=markups.accept_keyboard)

    logic.network_choice('tiktok')
    await botStates.AcceptButtons.accept.set()


# Confirming or canceling the deletion of the lists
@dp.message_handler(state=botStates.AcceptButtons.accept)
async def accept_ot_cancel(message: types.Message, state:FSMContext):
    with open('Dicts/relevant_network.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    relevant_network = data['relevant_network']
    answer = message.text

    if relevant_network == 'instagram':
        await message.answer('Instagram list is empty\n'
                             f'{texts.under_development}',
                             reply_markup=markups.delete_keyboard)
        await state.finish()

    elif relevant_network == 'youtube':
        if answer == "Accept ✅":
            logic.youtube_list_deleting(message.from_user.id)
            await message.answer(f'<b>{texts.accept_message}</b>',
                                 reply_markup=markups.delete_keyboard)
            await state.finish()
        elif answer == "Cancel 🚫":
            await message.answer(f'<b>{texts.cancel_message}</b>',
                                 reply_markup=markups.delete_keyboard)
            await state.finish()
        else:
            await message.answer(f'<b>{texts.error_message}</b>',
                                 reply_markup=markups.delete_keyboard)
            await state.finish()

    elif relevant_network == 'tiktok':
        await message.answer('TikTok list is empty\n'
                             f'{texts.under_development}',
                             reply_markup=markups.delete_keyboard)
        await state.finish()


# Feedback + FSM
@dp.message_handler(commands=['recommendation'])
@rate_limit(10)
async def feedback_message(message: types.Message):
    await message.answer(f'<b>{texts.feedback_message}</b>',
                         reply_markup=types.ReplyKeyboardRemove())

    await botStates.Feedback.recommendation.set()


# Receiving and confirming feedback text
@dp.message_handler(state=botStates.Feedback.recommendation)
async def feedback_editor(message: types.Message, state: FSMContext):
    feedback = message.text

    await state.update_data(user_feedback=feedback)
    await message.answer(f'💙 <u><b>Your Feedback</b></u> 💛\n\n'
                         f'[+] {feedback}',
                         reply_markup=markups.accept_keyboard)

    await botStates.Feedback.accept.set()


# Confirm feedback and send
@dp.message_handler(state=botStates.Feedback.accept)
async def feedback_accept(message: types.Message, state: FSMContext):
    accept_of_feedback = message.text

    if accept_of_feedback == 'Accept ✅':
        data = await state.get_data()
        accepted_feedback = data.get('user_feedback')

        await bot.send_message(CHANNEL_ID,
                               f'<b>Bot:</b> {texts.for_feedback}\n\n'
                               f'<b>Sender id:</b> <u>{message.from_user.id}\n</u>'
                               f'<b>Sender username:</b> @{message.from_user.username}\n\n'
                               f'<b>Message 📬</b>\n'
                               f'[+] {accepted_feedback}')

        await message.answer(f'<b>{texts.succesfully_sent_recommendation}</b>',
                             reply_markup=markups.start_keyboard)
        await state.finish()

    elif accept_of_feedback == 'Cancel 🚫':
        await message.answer(f'<b>{texts.cancel_recommendation_sending}</b>',
                             reply_markup=markups.start_keyboard)
        await state.finish()

    else:
        await message.answer(f'<b>{texts.error_message}</b>',
                             reply_markup=markups.start_keyboard)
        await state.finish()


# Echo reply to all third-party messages/commands
@dp.message_handler()
@rate_limit(1) # Ability to send a request every 2 seconds
async def echo_replys(message: types.Message):
    await message.answer(f'<b>{texts.echo_replys}</b>')


# Starting the bot and its functions
if __name__ == '__main__':
    # Start anti-spam
    dp.middleware.setup(ThrottlingMiddleware())

    # Launching the bot
    executor.start_polling(dp)
