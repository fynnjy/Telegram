from aiogram.dispatcher.filters.state import StatesGroup, State


class AddUser(StatesGroup):
    inst_user = State()
    yt_link = State()
    tt_link = State()


class DeleteUser(StatesGroup):
    inst_user = State()
    yt_user = State()
    tt_user = State()


class Feedback(StatesGroup):
    recommendation = State()
    accept = State()


class AcceptButtons(StatesGroup):
    accept = State()
