from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def order_keyboard(lang):
    if lang == 'uz':
        buttons = ["Buyurtma berish", "Buyurtma holati", "Sozlamalar"]
    else:
        buttons = ["Place Order", "Order Status", "Settings"]

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard
