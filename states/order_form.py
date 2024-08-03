from aiogram.dispatcher.filters.state import State, StatesGroup


class OrderForm(StatesGroup):
    direction = State()
    day = State()
    hour = State()
    passengers = State()
    additional_service = State()
    description = State()
    location = State()
