from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from config import TOKEN, CHANNEL_ID

import keyboards as keys
from Middlewares.rateLimits import rate_limit
from Middlewares.throttling import ThrottlingMiddleware
from botStates import Recommendations
from botStates import IPChecker
from checker import get_info_by_ip

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
    hello_message = "<b>Привіт 👋 Це - IP Checker 🤖</b>\n\n" \
                    "У ньому ти можеш отримати цікаву інформацію, " \
                    "вказавши потрібну тобі IP адресу. \n\n" \
                    "Якщо ти не знаєш, як її отримати, тисни " \
                    "'Створити лінк ⚡' нижче 👇 \n\n" \
                    "З усіх питань ви можете " \
                    "звернутися до адміністрації бота 🙋\n\n"

    await message.answer_sticker('CAACAgIAAxkBAAEEbtNiUw6G51T2xm5_p5Y7FLZdvBSyLwACm_0AAmOLRgySbtx7CqRIBSME')
    await message.answer(hello_message, reply_markup=keys.main_keyboard)


# Функция взятия необходимого IP + вход в первое состояние
@dp.message_handler(Text(equals='Дізнатися за IP 💻'), state=None)
@rate_limit(10) # 10с ограничитель-антиспам
async def get_info(message: types.Message):
    await message.answer('Введи IP адресу, яка тебе цікавить 🤖', reply_markup=types.ReplyKeyboardRemove())

    await IPChecker.send_ip.set()


# Состояние приема IP от пользователя
@dp.message_handler(state=IPChecker.send_ip)
async def answer_ip_info(message: types.Message, state: FSMContext):
    answer_ip = message.text

    try:
        get_info_by_ip(answer_ip)

        with open('Checked IP/checked_ip_file.json') as file:
            checkd_info = json.load(file)

        info = f"<b>💙 Отримана інформація 💛</b>\n\n" \
               f"<b>IP :</b> {checkd_info['[IP]']}\n" \
               f"<b>Провайдер :</b> {checkd_info['[Провайдер]']}\n" \
               f"<b>Організація :</b> {checkd_info['[Організація]']}\n" \
               f"<b>Країна :</b> {checkd_info['[Країна]']}\n" \
               f"<b>Назва регіону :</b> {checkd_info['[Назва регіону]']}\n" \
               f"<b>Місто :</b> {checkd_info['[Місто]']}\n" \
               f"<b>Поштовий код :</b> {checkd_info['[Поштовий код]']}\n" \
               f"<b>Ширина :</b> {checkd_info['[Ширина]']}\n" \
               f"<b>Довгота :</b> {checkd_info['[Довгота]']}\n\n" \
               f"<b>Нижче додано файл-посилання на мапу 🗺️</b>\n" \
               f"<b>Користуйся цією інформацією з розумом</b> 🧠"

        await message.answer(info)
        ip_map = open('Checked IP/checked_ip_map.html')
        await message.answer_document(ip_map, reply_markup=keys.main_keyboard)

        await bot.send_message(CHANNEL_ID, info)
        await state.finish()

    except:
        await message.answer('Перевір правильність введених данних 🤖', reply_markup=keys.main_keyboard)
        await state.finish()


# Функция-инструкция к ip-logger
@dp.message_handler(Text(equals='Створити лінк ⚡'))
@rate_limit(10) # 10с ограничитель-антиспам
async def logger_of_ip(message: types.Message):
    info_message = f'💙 <b>Коротка інструкція, як дізнатися IP адресу</b> 💛\n\n' \
                   f'Для початку тобі буде потрібно зайти на сайт 👇\n' \
                   f'<b>IP Logger</b> - https://iplogger.org/\n\n' \
                   f'Після переходу ви побачите поле, у яке вам потрібно ' \
                   f'ввести будь яке посилання та натиснути <b><u>Enter</u></b>, наприклад: \n' \
                   f'<b>Google</b> - https://google.com (тільки посилання) 🛸\n\n' \
                   f'Ви потрапите в кабінет, у якому буде відображатися ' \
                   f'статистика переходів за вашим посиланням та IP адреси людей, ' \
                   f'які переходили 🤫\n\n' \
                   f'Далі, задля того, щоб приховати основний сайт, бажано скоротити ' \
                   f'ваше посилання. У цьому вам доможе будь-який ресурс. Для прикладу ' \
                   f'візьмемо: \n' \
                   f'<b>Hyperhost</b> - https://hyperhost.ua/tools/ru/surli \n\n' \
                   f'Вводити своє посилання та скорочуєте його ⚡ Після чого можете ' \
                   f'відправити його людині та отримати IP адресу через кабінет <b>IP Logger</b> 🤖'

    await message.answer(info_message)


# Команда советов для администрации - переход в машину состояний
@dp.message_handler(commands=['recommendation'])
@rate_limit(300)  # Возможность отправки сообщений раз 5 минут
async def write_recommendation(message: types.Message):
    await message.answer("Дякую за зворотній зв'язок! Він допомагає робити бота кращим 💛\n\n"
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
@rate_limit(300)  # Возможность отправки сообщений раз 5 минут
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
    await message.answer(f'💙 <b>Ваше повідомлення</b> 💛\n\n[+] {answer}', reply_markup=keys.okno_keyboard)

    # Переход к слеующему этапу машины- состояний
    await Recommendations.accept.set()


# Уточнения корректности ответа о помощи
@dp.message_handler(state=Recommendations.help)
async def accept_recommendation(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(answer_recommendation=answer)
    await message.answer(f'💙 <b>Ваше повідомлення</b> 💛\n\n[+] {answer}', reply_markup=keys.okno_keyboard)

    # Переход к слеующему этапу машины- состояний
    await Recommendations.accept.set()


@dp.message_handler(state=Recommendations.accept)
async def send_recommendation(message: types.Message, state: FSMContext):
    answer_2 = message.text

    if answer_2 == 'Надіслати ✅':
        data = await state.get_data()
        rec = data.get('answer_recommendation')

        await bot.send_message(CHANNEL_ID, f'<b>💙 IP Checker 💛</b>\n\n <u>Сообщение:</u>\n {rec}')
        await message.answer('Ваше повідомлення успішно надіслано ✅')
        await asyncio.sleep(0.5)
        await state.finish()
    elif answer_2 == 'Скасувати 🚫':
        await state.finish()
    else:
        await message.answer('Щось пішло не так 🤖')
        await state.finish()

    await message.answer('Ви повернулися до основного розділу 🙋', reply_markup=keys.main_keyboard)


# Эхо-ответ на все сторонний сообщения / команды
@dp.message_handler()
@rate_limit(5)  # Возможность отправки сообщений раз 5 секунд
async def news_tracker(message: types.Message):
    await message.answer("Вибачте, наразі бот не вміє "
                         "спілкуватися з користувачами 🤖")


# Запуск бота
if __name__ == '__main__':
    # Запуск антиспама
    dp.middleware.setup(ThrottlingMiddleware())

    # Запуск бота
    executor.start_polling(dp)