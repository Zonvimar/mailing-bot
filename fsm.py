from aiogram.dispatcher.filters.state import State, StatesGroup


class Mailing(StatesGroup):
    text = State()
    text2 = State()
    number_gr = State()


