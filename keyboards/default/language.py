from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def language_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('O\'zbekcha 🇺🇿'), KeyboardButton('English 🇺🇸'))
    return keyboard
