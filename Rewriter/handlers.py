from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Middlewares.throttling import ThrottlingMiddleware
from Keyboards.InlineKeyboards import inline_keyboard
from Keyboards.ReplyKeyboards import reply_keyboard
from aiogram.types import ContentType, CallbackQuery
from aiogram import Bot, Dispatcher, executor, types
from Middlewares.rateLimits import rate_limit
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from config import TOKEN, CHANNEL_ID
from aiogram.types import Message
import write_or_file
import translation
import textsaver
import logging
import texts
import fsm

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
@rate_limit(600)
async def start_working(message: Message):
    await message.answer_sticker(texts.start_sticker)
    await message.answer(f'<b>Hi, {message.from_user.username} 👋\n\n</b>'
                         f'{texts.start_message}',
                         reply_markup=reply_keyboard.start_keyboard)


@dp.message_handler(Text(equals='Enter text 🖋'), state=None)
@rate_limit(1)
async def text_input(message: Message):
    await message.answer(texts.text_input_message,
                         reply_markup=types.ReplyKeyboardRemove())

    await message.delete()
    await fsm.TextToTranslate.personal_text.set()


@dp.message_handler(state=fsm.TextToTranslate.personal_text)
async def users_text(message: Message, state: FSMContext):
    answer = message.text
    if len(answer) > 4000:
        await message.answer(texts.text_limit,
                             reply_markup=reply_keyboard.start_keyboard)
        await state.finish()

    else:
        await message.answer(texts.translate_to,
                             reply_markup=inline_keyboard.text_translation)

        textsaver.user_text_saver(answer)
        write_or_file.variant("text")
        await state.finish()


@dp.message_handler(Text(equals='Send file ✉️'), state=None)
@rate_limit(1)
async def file_input(message: Message):
    await message.answer(texts.file_input_message,
                         reply_markup=types.ReplyKeyboardRemove())

    await message.delete()
    await fsm.FileToTranslate.personal_file.set()


@dp.message_handler(state=fsm.FileToTranslate.personal_file,
                    content_types=ContentType.ANY)
async def users_file(message: Message, state: FSMContext):
    if message.content_type == ContentType.DOCUMENT:
        await message.answer(texts.translate_to,
                             reply_markup=inline_keyboard.text_translation)

        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, "UserTexts/user_file.txt")

        with open("UserTexts/user_file.txt", "r", encoding="utf-8") as file:
            textsaver.user_text_saver(file.read())

        write_or_file.variant("file")

        await state.finish()

    else:
        await message.answer(texts.error_message,
                             reply_markup=reply_keyboard.start_keyboard)
        await state.finish()


@dp.callback_query_handler(text_contains="to_ua")
@rate_limit(1)
async def to_ukrainian(call: CallbackQuery):
    await call.answer(texts.translate_to_ukrainian)
    await call.message.delete()

    await call.message.answer_sticker(texts.final_sticker)

    if write_or_file.check_status() == "text":
        await call.message.answer(f'{translation.translation_process("uk")}',
                                  reply_markup=reply_keyboard.start_keyboard)

    elif write_or_file.check_status() == "file":
        translation.translation_process("uk")

        user_file = types.MediaGroup()
        user_file.attach_document(types.InputFile("UserTexts/rewrote.txt"))

        await call.message.answer(f'<b>{texts.wait_message}</b>',
                                  reply_markup=reply_keyboard.start_keyboard)

        await bot.send_media_group(call.message.chat.id, media=user_file)

    else:
        await call.message.answer("Something went wrong")


@dp.callback_query_handler(text_contains="to_en")
@rate_limit(1)
async def to_english(call: CallbackQuery):
    await call.answer(texts.translate_to_english)
    await call.message.delete()

    await call.message.answer_sticker(texts.final_sticker)

    if write_or_file.check_status() == "text":
        await call.message.answer(f'{translation.translation_process("en")}',
                                  reply_markup=reply_keyboard.start_keyboard)

    elif write_or_file.check_status() == "file":
        translation.translation_process("en")

        user_file = types.MediaGroup()
        user_file.attach_document(types.InputFile("UserTexts/rewrote.txt"))

        await call.message.answer(f'<b>{texts.wait_message}</b>',
                                  reply_markup=reply_keyboard.start_keyboard)

        await bot.send_media_group(call.message.chat.id, media=user_file)

    else:
        await call.message.answer("Something went wrong")


@dp.callback_query_handler(text_contains="to_fr")
@rate_limit(1)
async def to_french(call: CallbackQuery):
    await call.answer(texts.translate_to_french)
    await call.message.delete()

    await call.message.answer_sticker(texts.final_sticker)

    if write_or_file.check_status() == "text":
        await call.message.answer(f'{translation.translation_process("fr")}',
                                  reply_markup=reply_keyboard.start_keyboard)

    elif write_or_file.check_status() == "file":
        translation.translation_process("fr")

        user_file = types.MediaGroup()
        user_file.attach_document(types.InputFile("UserTexts/rewrote.txt"))

        await call.message.answer(f'<b>{texts.wait_message}</b>',
                                  reply_markup=reply_keyboard.start_keyboard)

        await bot.send_media_group(call.message.chat.id, media=user_file)

    else:
        await call.message.answer("Something went wrong")


@dp.callback_query_handler(text_contains="to_pl")
@rate_limit(1)
async def to_polish(call: CallbackQuery):
    await call.answer(texts.translate_to_polish)
    await call.message.delete()

    await call.message.answer_sticker(texts.final_sticker)

    if write_or_file.check_status() == "text":
        await call.message.answer(f'{translation.translation_process("pl")}',
                                  reply_markup=reply_keyboard.start_keyboard)

    elif write_or_file.check_status() == "file":
        translation.translation_process("pl")

        user_file = types.MediaGroup()
        user_file.attach_document(types.InputFile("UserTexts/rewrote.txt"))

        await call.message.answer(f'<b>{texts.wait_message}</b>',
                                  reply_markup=reply_keyboard.start_keyboard)

        await bot.send_media_group(call.message.chat.id, media=user_file)

    else:
        await call.message.answer("Something went wrong")


@dp.callback_query_handler(text_contains="to_de")
@rate_limit(1)
async def to_german(call: CallbackQuery):
    await call.answer(texts.translate_to_german)
    await call.message.delete()

    await call.message.answer_sticker(texts.final_sticker)

    if write_or_file.check_status() == "text":
        await call.message.answer(f'{translation.translation_process("de")}',
                                  reply_markup=reply_keyboard.start_keyboard)

    elif write_or_file.check_status() == "file":
        translation.translation_process("de")

        user_file = types.MediaGroup()
        user_file.attach_document(types.InputFile("UserTexts/rewrote.txt"))

        await call.message.answer(f'<b>{texts.wait_message}</b>',
                                  reply_markup=reply_keyboard.start_keyboard)

        await bot.send_media_group(call.message.chat.id, media=user_file)

    else:
        await call.message.answer("Something went wrong")


# Feedback + FSM
@dp.message_handler(commands=['recommendation'])
@rate_limit(10)
async def feedback_message(message: types.Message):
    await message.delete()
    await message.answer(f'<b>{texts.feedback_message}</b>',
                         reply_markup=types.ReplyKeyboardRemove())

    await fsm.Feedback.recommendation.set()


# Receiving and confirming feedback text
@dp.message_handler(state=fsm.Feedback.recommendation, content_types=ContentType.ANY)
async def feedback_editor(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await message.delete()
        feedback = message.text

        await state.update_data(user_feedback=feedback)
        await message.answer(f'💙 <u><b>Your Feedback</b></u> 💛\n\n'
                             f'[+] {feedback}',
                             reply_markup=reply_keyboard.accept_keyboard)

        await fsm.Feedback.accept.set()

    else:
        await message.answer(texts.error_message,
                             reply_markup=reply_keyboard.start_keyboard)
        await state.finish()


# Confirm feedback and send
@dp.message_handler(state=fsm.Feedback.accept)
async def feedback_accept(message: types.Message, state: FSMContext):
    await message.delete()
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

        await message.answer(f'<b>{texts.successfully_sent_recommendation}</b>',
                             reply_markup=reply_keyboard.start_keyboard)
        await state.finish()

    elif accept_of_feedback == 'Cancel 🚫':
        await message.answer(f'<b>{texts.cancel_recommendation_sending}</b>',
                             reply_markup=reply_keyboard.start_keyboard)
        await state.finish()

    else:
        await message.answer(f'<b>{texts.error_message}</b>',
                             reply_markup=reply_keyboard.start_keyboard)
        await state.finish()


# Echo reply on all any messages
@dp.message_handler(content_types=ContentType.ANY)
@rate_limit(1)
async def sticker_answer(message: Message):
    await message.answer(texts.echo_reply)


# Starting the bot and its functions
if __name__ == '__main__':
    # Start anti-spam
    dp.middleware.setup(ThrottlingMiddleware())

    # Launching the bot
    executor.start_polling(dp)
