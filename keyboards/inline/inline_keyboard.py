from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def direction_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Farg'ona - Toshkent", callback_data="dir_ft"))
    keyboard.add(InlineKeyboardButton("Toshkent - Farg'ona", callback_data="dir_tf"))
    keyboard.add(InlineKeyboardButton("Asosiy menyu", callback_data="main_menu"))
    keyboard.add(InlineKeyboardButton("Ortga qaytish", callback_data="back"))
    return keyboard


def day_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Bugun", callback_data="today"))
    keyboard.add(InlineKeyboardButton("Ertaga", callback_data="tomorrow"))
    keyboard.add(InlineKeyboardButton("Asosiy menyu", callback_data="main_menu"))
    keyboard.add(InlineKeyboardButton("Ortga qaytish", callback_data="back"))
    return keyboard


def time_keyboard(hours):
    keyboard = InlineKeyboardMarkup()
    for hour in hours:
        keyboard.add(InlineKeyboardButton(f"{hour}:00", callback_data=f"time_{hour}"))
    keyboard.add(InlineKeyboardButton("Asosiy menyu", callback_data="main_menu"))
    keyboard.add(InlineKeyboardButton("Ortga qaytish", callback_data="back"))
    return keyboard


def passengers_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("1", callback_data="passenger_1"))
    keyboard.add(InlineKeyboardButton("2", callback_data="passenger_2"))
    keyboard.add(InlineKeyboardButton("3", callback_data="passenger_3"))
    keyboard.add(InlineKeyboardButton("4", callback_data="passenger_4"))
    keyboard.add(InlineKeyboardButton("Asosiy menyu", callback_data="main_menu"))
    keyboard.add(InlineKeyboardButton("Ortga qaytish", callback_data="back"))
    return keyboard


def additional_service_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Old o'rindiq", callback_data="service_front_seat"))
    keyboard.add(InlineKeyboardButton("Ayol kishi", callback_data="service_female"))
    keyboard.add(InlineKeyboardButton("Konditsioner", callback_data="service_ac"))
    keyboard.add(InlineKeyboardButton("Tomda bagaj", callback_data="service_roof_bag"))
    keyboard.add(InlineKeyboardButton("Davom etish", callback_data="continue"))
    keyboard.add(InlineKeyboardButton("Asosiy menyu", callback_data="main_menu"))
    keyboard.add(InlineKeyboardButton("Ortga qaytish", callback_data="back"))
    return keyboard


def default_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Asosiy menyu", callback_data="main_menu"))
    keyboard.add(InlineKeyboardButton("Ortga qaytish", callback_data="back"))
    return keyboard
