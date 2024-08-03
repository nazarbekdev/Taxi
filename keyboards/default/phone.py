from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def phone_keyboard(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'uz':
        button = KeyboardButton('Raqamni ulashish', request_contact=True)
    else:
        button = KeyboardButton('Share phone number', request_contact=True)
    keyboard.add(button)
    return keyboard
