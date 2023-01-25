from aiogram.dispatcher.filters.state import StatesGroup, State


class WeatherStates(StatesGroup):
    city = State()


class Recommendations(StatesGroup):
    recommendation = State()
    help = State()
    accept = State()
