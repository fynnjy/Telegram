from aiogram.dispatcher.filters.state import StatesGroup, State


class Recommendations(StatesGroup):
    recommendation = State()
    help = State()
    accept = State()


class IPChecker(StatesGroup):
    send_ip = State()
