from aiogram import types
from loader import dp


@dp.message_handler(lambda message: message.text in ["Buyurtma berish", "Place Order"])
async def place_order(message: types.Message):
    await message.answer("Buyurtma berish funksiyasi hozircha mavjud emas.")


@dp.message_handler(lambda message: message.text in ["Buyurtma holati", "Order Status"])
async def order_status(message: types.Message):
    await message.answer("Buyurtma holati funksiyasi hozircha mavjud emas.")


@dp.message_handler(lambda message: message.text in ["Sozlamalar", "Settings"])
async def settings(message: types.Message):
    await message.answer("Sozlamalar funksiyasi hozircha mavjud emas.")
