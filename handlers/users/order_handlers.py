from aiogram import types
from loader import dp
from aiogram.dispatcher import FSMContext
from states.order_form import OrderForm
from keyboards.inline.inline_keyboard import direction_keyboard, day_keyboard, time_keyboard, passengers_keyboard, \
    additional_service_keyboard, default_keyboard
from keyboards.default.order_keyboard import order_keyboard
import requests
from data.config import API_URL_ORDER
import datetime


@dp.callback_query_handler(lambda c: c.data == 'main_menu', state='*')
async def main_menu(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language', 'uz')
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer("Asosiy menyu", reply_markup=order_keyboard(lang))
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'back', state='*')
async def go_back(callback_query: types.CallbackQuery, state: FSMContext):
    state_name = await state.get_state()
    if state_name == OrderForm.day.state:
        await OrderForm.previous()
        await callback_query.message.edit_text("Qayerga borishni xohlaysiz?", reply_markup=direction_keyboard())
    elif state_name == OrderForm.hour.state:
        await OrderForm.previous()
        await callback_query.message.edit_text("Qaysi kuni borishni rejalashtiryapsiz?", reply_markup=day_keyboard())
    elif state_name == OrderForm.passengers.state:
        await OrderForm.previous()
        await callback_query.message.edit_text("Qaysi soatda borishni rejalashtiryapsiz?",
                                               reply_markup=time_keyboard([str(hour) for hour in range(14, 24)]))
    elif state_name == OrderForm.additional_service.state:
        await OrderForm.previous()
        await callback_query.message.edit_text("Necha kishi boradi?", reply_markup=passengers_keyboard())
    elif state_name == OrderForm.description.state:
        await OrderForm.previous()
        await callback_query.message.edit_text("Qo'shimcha xizmatlar bormi?",
                                               reply_markup=additional_service_keyboard())
    elif state_name == OrderForm.location.state:
        await OrderForm.previous()
        await callback_query.message.edit_text("Qo'shimcha tavsifni kiriting:", reply_markup=default_keyboard())


@dp.message_handler(lambda message: message.text in ["Buyurtma berish", "Place Order"])
async def place_order(message: types.Message, state: FSMContext):
    await message.answer("Qayerga borishni xohlaysiz?", reply_markup=direction_keyboard())
    # await message.answer(" ", reply_markup=types.ReplyKeyboardRemove())
    await OrderForm.direction.set()


@dp.callback_query_handler(state=OrderForm.direction)
async def set_direction(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data in ["dir_ft", "dir_tf"]:
        await state.update_data(direction=callback_query.data)
        await callback_query.message.edit_text("Qaysi kuni borishni rejalashtiryapsiz?", reply_markup=day_keyboard())
        await OrderForm.next()
    elif callback_query.data == 'main_menu':
        await main_menu(callback_query, state)
    elif callback_query.data == 'back':
        await go_back(callback_query, state)


@dp.callback_query_handler(state=OrderForm.day)
async def set_day(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data in ["today", "tomorrow"]:
        await state.update_data(day=callback_query.data)

        now = datetime.datetime.now()
        if callback_query.data == "today":
            hours = [str(hour) for hour in range(now.hour + 1, 24)]
        else:
            hours = [str(hour) for hour in range(0, 24)]

        await callback_query.message.edit_text("Qaysi soatda borishni rejalashtiryapsiz?",
                                               reply_markup=time_keyboard(hours))
        await OrderForm.next()
    elif callback_query.data == 'main_menu':
        await main_menu(callback_query, state)
    elif callback_query.data == 'back':
        await go_back(callback_query, state)


@dp.callback_query_handler(state=OrderForm.hour)
async def set_hour(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.startswith("time_"):
        hour = callback_query.data.split("_")[1]
        await state.update_data(hour=hour)
        await callback_query.message.edit_text("Necha kishi boradi?", reply_markup=passengers_keyboard())
        await OrderForm.next()
    elif callback_query.data == 'main_menu':
        await main_menu(callback_query, state)
    elif callback_query.data == 'back':
        await go_back(callback_query, state)


@dp.callback_query_handler(state=OrderForm.passengers)
async def set_passengers(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.startswith("passenger_"):
        passengers = callback_query.data.split("_")[1]
        await state.update_data(passengers=passengers)
        await callback_query.message.edit_text("Qo'shimcha xizmatlar bormi?",
                                               reply_markup=additional_service_keyboard())
        await OrderForm.next()
    elif callback_query.data == 'main_menu':
        await main_menu(callback_query, state)
    elif callback_query.data == 'back':
        await go_back(callback_query, state)


@dp.callback_query_handler(state=OrderForm.additional_service)
async def set_additional_service(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.startswith("service_"):
        data = await state.get_data()
        additional_services = data.get('additional_services', [])
        additional_services.append(callback_query.data.split("_")[1])
        await state.update_data(additional_services=additional_services)
        await callback_query.message.edit_text("Qo'shimcha xizmatlar bormi?",
                                               reply_markup=additional_service_keyboard())
    elif callback_query.data == 'continue':
        await callback_query.message.edit_text("Qo'shimcha tavsifni kiriting:", reply_markup=default_keyboard())
        await OrderForm.next()
    elif callback_query.data == 'main_menu':
        await main_menu(callback_query, state)
    elif callback_query.data == 'back':
        await go_back(callback_query, state)


@dp.message_handler(state=OrderForm.description)
async def set_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Joylashuvingizni kiriting:", reply_markup=default_keyboard())
    await OrderForm.next()


@dp.message_handler(state=OrderForm.location)
async def set_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)

    data = await state.get_data()
    print(data)

    order_data = {
        'user_id': str(message.from_user.id),
        'direction': data['direction'],
        'day': data['day'],
        'hour': data['hour'],
        'passengers': data['passengers'],
        'additional_service': ', '.join(data.get('additional_services', [])),
        'description': data['description'],
        'location': data['location']
    }

    resp = requests.post(url=API_URL_ORDER, data=order_data)
    if resp.status_code == 200:
        await message.answer(' Buyurtmangiz qabul qilindi')
    else:
        await message.answer(' Buyurtma berish amalga oshmadi')
    await state.finish()
