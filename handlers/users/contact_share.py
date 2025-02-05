from aiogram import types
from keyboards.default.order_keyboard import order_keyboard
from loader import dp
from data.translations import translations
from keyboards.default.phone import phone_keyboard
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import requests
from data.config import API_URL
from states.form import Form


@dp.message_handler(lambda message: message.text in ['O\'zbekcha 🇺🇿', 'English 🇺🇸'])
async def set_language(message: types.Message, state: FSMContext):
    if message.text == 'O\'zbekcha 🇺🇿':
        lang = 'uz'
    else:
        lang = 'en'
    resp = requests.post(url='http://localhost:8000/api/v1/user-language', data={'user_id': message.from_user.id, 'lan': lang})
    if resp.status_code == 200:
        await state.update_data(language=lang)
        await message.answer(translations[lang]['share_phone'], reply_markup=phone_keyboard(lang))
        await Form.phone.set()
    else:
        await message.answer('Siz oldin ro\'yxatdan o\'tgansiz!')


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.phone)
async def contact_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language', 'uz')
    contact = message.contact
    await state.update_data(phone_number=contact.phone_number, user_id=contact.user_id)
    await message.answer(translations[lang]['name_prompt'], reply_markup=types.ReplyKeyboardRemove())
    await Form.name.set()


@dp.message_handler(state=Form.name)
async def name_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language', 'uz')
    phone_number = data.get('phone_number')
    user_id = data.get('user_id')
    name = message.text


    payload = {
        'user_id': user_id,
        'name': name,
        'phone_number': phone_number
    }
    resp = requests.post(url=API_URL, data=payload)
    if resp.status_code == 200:
        await message.answer(translations[lang]['name_received'], reply_markup=order_keyboard(lang))
    elif resp.status_code == 400:
        await message.answer('xato emas', reply_markup=order_keyboard(lang))
    else:
        await message.answer("An error occurred while saving your data. Please try again. \n/start")

    await state.finish()
