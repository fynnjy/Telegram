from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from main_parser import news_unian, updates_unian
from main_parser import news_rbc, updates_rbc
from main_parser import news_bbc, updates_bbc
from main_parser import get_currency

from botStates import WeatherStates
from botStates import Recommendations

from config import TOKEN, user_id
from config import weather_api
from config import CHANNEL_ID

import markups as kups
from Middlewares.rateLimits import rate_limit
from Middlewares.throttling import ThrottlingMiddleware

from datetime import date
import requests
import logging
import asyncio
import json

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


# Начало работы бота по комманде Start
@dp.message_handler(commands=['start'])
@rate_limit(600)  # Возможность отправки сообщений раз 10 минут
async def start_bot(message: types.Message):
    hello_message = "Ласкаво просимо до UkrInfoBot 🤖\n\n" \
                    "Цей бот покликаний зробити пошук актуальних новин, " \
                    "відстеження цікавих для вас ресурсів і заходів " \
                    "максимально простим та ефективним! \n\n" \
                    "З усіх питань ви можете " \
                    "звернутися до адміністрації бота 🙋\n\n"

    await message.answer_sticker('CAACAgIAAxkBAAEEbtNiUw6G51T2xm5_p5Y7FLZdvBSyLwACm_0AAmOLRgySbtx7CqRIBSME')
    await message.answer(hello_message, reply_markup=kups.main_keyboard)

    await asyncio.sleep(2)
    await message.answer('Йде пошук актуальних новин 🔎')
    await asyncio.sleep(5)

    # Функция сбора новостей из Униан-а
    news_unian()

    with open("dicts/newsUnian.json", encoding="utf-8") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f"<b>🔹Час публікації: {v['news_time']}</b>\n" \
               f"🔸<b>Тема</b>: {v['news_title']}\n\n" \
               f"{hlink(v['ulr_title'], v['news_url'])}"

        await message.answer(news)

    await asyncio.sleep(2)
    await message.answer('Увімкнено режим автоматичного пошуку новин 🤖')

    # Функция сбора новостей их РБК
    news_rbc()

    # Функция сбора новостей их BBC
    news_bbc()


# Вход во второе меню для выбора других источников новостей
@dp.message_handler(Text(equals='Інші ресурси ⤵'))
async def info_tariff(message: types.Message):
    await message.answer('У цьому розділі ви можете переглянути новини з інших інформаційних ресурсів 🗓',
                         reply_markup=kups.second_keyboard)


# Выход в основное меню
@dp.message_handler(Text(equals='Назад ⬅'))
async def back_to_main_menu(message: types.Message):
    await message.answer('Ви повернулися до основного розділу 🙋', reply_markup=kups.main_keyboard)


# Поиск свежих новостей вызванный кнопкой
@dp.message_handler(Text(equals="Новини 🔖"))
@rate_limit(300)  # Возможность отправки сообщений раз 5 минут
async def get_freshnews_only(message: types.Message):
    fresh_news = updates_unian()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"<b>🔹Час публікації: {v['news_time']}</b>\n" \
                   f"🔸<b>Тема</b>: {v['news_title']}\n\n" \
                   f"{hlink(v['ulr_title'], v['news_url'])}"

            await message.answer(news)
    else:
        await message.answer('Поки що немає нічого нового 🤖')
        await asyncio.sleep(0.5)
        await message.answer('Останні актуальні новини 🗃️')
        await asyncio.sleep(1.5)

        with open("dicts/newsUnian.json", encoding="utf-8") as file:
            news_dict = json.load(file)

        for k, v in sorted(news_dict.items())[-2:]:
            news = f"<b>🔹Час публікації: {v['news_time']}</b>\n" \
                   f"🔸<b>Тема</b>: {v['news_title']}\n\n" \
                   f"{hlink(v['ulr_title'], v['news_url'])}"

            await message.answer(news)
            await asyncio.sleep(0.2)


# Поиск новых новостей каждые 10 секунд
async def news_every_minute():
    while True:
        fresh_news = updates_unian()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"<b>🔹Час публікації: {v['news_time']}</b>\n" \
                       f"🔸<b>Тема</b>: {v['news_title']}\n\n" \
                       f"{hlink(v['ulr_title'], v['news_url'])}"

                # @userinfobot
                # await bot.send_sticker(user_id, 'CAACAgIAAxkBAAEEl6JibGAsnR5Cpq310Gq1Wu'
                #                                 'VrLntBjQACshQAAgJHKUvbRQzuhBMcuyQE')
                await bot.send_message(user_id, news)
        # При отсутствии новостей
        # else:
        #     await bot.send_message(user_id, "Поки що нових новин немає 🤖",
        #                            disable_notification=True)

        await asyncio.sleep(90)


# Прогноз погоды -> переход в машину состояний
@dp.message_handler(Text(equals="Погода 💧"), state=None)
@rate_limit(4)  # Возможность отправки сообщений раз 4 секунды
async def search_weather(message: types.Message):
    await message.answer('Введіть місто 🤖', reply_markup=types.ReplyKeyboardRemove())

    await WeatherStates.city.set()


# Состояние ожидание ответа - город
@dp.message_handler(state=WeatherStates.city)
async def answer_city(message: types.Message, state: FSMContext):
    answer = message.text

    try:
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?'
                         f'q={answer}&appid={weather_api}&units=metric')
        data = r.json()

        city = data['name']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        wind_speed = data['wind']['speed']

        await message.answer(f'🔹<b>Зараз у {city} {temperature}</b>℃🔸\n\n'
                             f'📉 Мінімальна<b>:</b> {temp_min}℃\n'
                             f'📈 Максимальна<b>:</b> {temp_max}℃\n'
                             f'🌤 Відчувається як<b>:</b> {feels_like}℃\n\n'
                             f'💧 Вологість<b>:</b> {humidity}\n'
                             f'🌡 Тиск<b>:</b> {pressure}\n'
                             f'💨 Швидкість вітру<b>:</b> {wind_speed}', reply_markup=kups.main_keyboard)

        await state.finish()

    except:
        await message.answer('Місто вказано невірно 🤖', reply_markup=kups.main_keyboard)
        await state.finish()


# Актуальный курс валют
@dp.message_handler(Text(equals="Валюти 💰"))
@rate_limit(300)  # Возможность отправки сообщений раз 5 минут
async def currency(message: types.Message):
    get_currency()
    with open('dicts/currency_dict.json', encoding="utf-8") as file:
        currency_tg = json.load(file)

    for k, v in currency_tg.items():
        currencys = f"🔹<b>Співвідношення валют: {v['currency_name']} & UAH</b>🔸\n" \
                    f"<b>Покупка:</b> {v['currency_buy']}грн\n" \
                    f"<b>Продаж:</b> {v['currency_sale']}грн"

        await message.answer(currencys)

    finance = (f'Інформація взята з джерела: '
               f'{hlink("finance.ua", "https://finance.ua/banks/privatbank/currency")} 📌')

    await message.answer(finance, disable_web_page_preview=True)


# Получение новостей из РБК
@dp.message_handler(Text(equals='RBC🗞'))
@rate_limit(60)  # Возможность отправки сообщений раз 60 секунд
async def get_rbc_news(message: types.Message):
    fresh_news = updates_rbc()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items())[-10:]:
            news = f"<b>🔹Час публікації: {date.today()} {v['news_time']}</b>\n" \
                   f"🔸<b>Тема</b>: {v['news_title']}\n\n" \
                   f"Інформація взята з джерела: {hlink('rbc.ua', v['news_link'])} 📌"
            await message.answer(news)
    else:
        await message.answer('Останні актуальні новини 🗃️')
        await asyncio.sleep(1.5)

        with open('dicts/newsRbc.json', encoding="utf-8") as file:
            rbcNews_dict = json.load(file)

        for k, v in sorted(rbcNews_dict.items())[-2:]:
            news = f"<b>🔹Час публікації: {date.today()} {v['news_time']}</b>\n" \
                   f"🔸<b>Тема</b>: {v['news_title']}\n\n" \
                   f"Інформація взята з джерела: {hlink('rbc.ua', v['news_link'])} 📌"
            await message.answer(news)


# Получение новостей из BBC
@dp.message_handler(Text(equals='BBC🗞'))
@rate_limit(60)  # Возможность отправки сообщений раз 60 секунд
async def get_bbc_news(message: types.Message):
    fresh_news = updates_bbc()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items())[-5:]:
            news = f"<b>🔹Час публікації: {v['news_time']}</b>\n" \
                   f"🔸<b>Тема</b>: {v['news_title']}\n\n" \
                   f"Інформація взята з джерела: {hlink('bbc.com', v['news_url'])} 📌"
            await message.answer(news)
    else:
        await message.answer('Останні актуальні новини 🗃️')
        await asyncio.sleep(1.5)

        with open('dicts/newsBBC.json', encoding="utf-8") as file:
            newsBBC = json.load(file)

        for k, v in sorted(newsBBC.items())[-2:]:
            news = f"<b>🔹Час публікації: {v['news_time']}</b>\n" \
                   f"🔸<b>Тема</b>: {v['news_title']}\n\n" \
                   f"Інформація взята з джерела: {hlink('bbc.ua', v['news_url'])} 📌"
            await message.answer(news)


# Команда советов для администрации - переход в машину состояний
@dp.message_handler(commands=['recommendation'])
@rate_limit(10)  # Возможность отправки сообщений раз 10 секунд
async def write_recommendation(message: types.Message):
    await message.answer("Дякую за зворотній зв'язок!\nЦе допомагає робити бота кращим 💛\n\n"
                         "⠀• Бот приймає лише текстові повідомлення. "
                         "Будь ласка, утримайтеся від надсилання зайвої "
                         "інформації (стікерів, гіф, фото та аудіоповідомлень)❗\n\n"
                         "⠀• Ваше повідомлення буде надіслано анонімно 🛡 "
                         "Якщо ви бажаєте отримати зворотний зв'язок, "
                         "напишіть, будь ласка, свої контактні дані, за "
                         "якими з вами можна буде зв'язатися 🙏\n\n"
                         "⠀• Після надсилання повідомлення боту ви "
                         "зможете переглянути повідомлення та вирішити, "
                         "відправляти його чи ні ☑", reply_markup=types.ReplyKeyboardRemove())

    await Recommendations.recommendation.set()


# Команда помощи от администрации - переход в машину состояний
@dp.message_handler(commands=['help'])
@rate_limit(10)  # Возможность отправки сообщений раз 10 секунд
async def write_help(message: types.Message):
    await message.answer("Підкажіть, яка саме вам потрібна допомога? 🤖\n\n"
                         "⠀• Бот приймає лише текстові повідомлення. "
                         "Будь ласка, утримайтеся від надсилання зайвої "
                         "інформації (стікерів, гіф, фото та аудіоповідомлень)❗\n\n"
                         "⠀• Ваше повідомлення буде надіслано анонімно 🛡 "
                         "Якщо ви бажаєте отримати зворотний зв'язок, "
                         "напишіть, будь ласка, свої контактні дані, за "
                         "якими з вами можна буде зв'язатися 🙏\n\n"
                         "⠀• Після надсилання повідомлення боту ви зможете "
                         "переглянути повідомлення та вирішити, відправляти "
                         "його чи ні ☑", reply_markup=types.ReplyKeyboardRemove())

    await Recommendations.help.set()


# Уточнения корректности ответа рекоммендаций
@dp.message_handler(state=Recommendations.recommendation)
async def accept_recommendation(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(answer_recommendation=answer)
    await message.answer(f'💙 <b>Ваше повідомлення</b> 💛\n\n[+] {answer}',
                         reply_markup=kups.okno_keyboard)

    # Переход к слеующему этапу машины- состояний
    await Recommendations.accept.set()


# Уточнения корректности ответа о помощи
@dp.message_handler(state=Recommendations.help)
async def accept_recommendation(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(answer_recommendation=answer)
    await message.answer(f'💙 <b>Ваше повідомлення</b> 💛\n\n[+] {answer}',
                         reply_markup=kups.okno_keyboard)

    # Переход к слеующему этапу машины- состояний
    await Recommendations.accept.set()


# Отправить или отменить отправку сообщения в тех.поддержку
@dp.message_handler(state=Recommendations.accept)
async def send_recommendation(message: types.Message, state: FSMContext):
    answer_2 = message.text

    if answer_2 == 'Надіслати ✅':
        data = await state.get_data()
        rec = data.get('answer_recommendation')

        await bot.send_message(CHANNEL_ID, rec)
        await message.answer('Ваше повідомлення успішно надіслано ✅')
        await asyncio.sleep(0.5)
        await state.finish()
    elif answer_2 == 'Скасувати 🚫':
        await state.finish()
    else:
        await message.answer('Щось пішло не так 🤖')
        await state.finish()

    await message.answer('Ви повернулися до основного розділу 🙋',
                         reply_markup=kups.main_keyboard)


# Эхо-ответ на все сторонний сообщения / команды
@dp.message_handler()
@rate_limit(5)  # Возможность отправки сообщений раз 5 секунд
async def news_tracker(message: types.Message):
    await message.answer("Вибачте, наразі бот не вміє "
                         "спілкуватися з користувачами 🤖")


# Запуск бота и его функций
if __name__ == '__main__':
    # Запуск функции автоматического поиска
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(news_every_minute())

    # Запуск антиспама
    dp.middleware.setup(ThrottlingMiddleware())

    # Запуск бота
    executor.start_polling(dp)
