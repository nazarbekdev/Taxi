from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    phone = State()
    name = State()
