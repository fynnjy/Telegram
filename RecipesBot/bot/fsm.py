from telebot.handler_backends import State, StatesGroup


class AboutUser(StatesGroup):
    name = State()
    gender = State()
