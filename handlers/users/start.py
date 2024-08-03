from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.translations import translations
from keyboards.default.language import language_keyboard
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(translations['uz']['start'], reply_markup=language_keyboard())
