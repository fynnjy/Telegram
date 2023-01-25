from aiogram.dispatcher.filters.state import StatesGroup, State


class TextToTranslate(StatesGroup):
    personal_text = State()


class FileToTranslate(StatesGroup):
    personal_file = State()


class Feedback(StatesGroup):
    recommendation = State()
    accept = State()
