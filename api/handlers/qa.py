import time
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from api.loader import bot, dp, ds_admin, js_admin
from api.utils.checkers import email_checker, phone_checker
from api.utils import static_text as st
from api.utils import keyboard as kb
from states.user_data import UserData as ud
from spreadsheet.gt import table


@dp.message_handler(state=ud.came_to)
async def answer_q1(message: types.Message, state: FSMContext):
    """Первый вопрос.
    Узнали через кнопки на чьё DS\JS мероприятие пришёл пользователь.
    Просим вручную ввести его имя и фамилию для базы"""

    user_name = message.from_user.first_name
    # user_fullname = message.from_user.full_name
    # user_id = message.from_user.id    
    answer = message.text

    logging.info(f"from {user_name} answer {answer} at {time.strftime('%X %x')}")

    await state.update_data(came_to=answer)

    await message.answer(f"{st.NAME}", reply_markup=kb.main_menu)

    await ud.name_surname.set()

@dp.message_handler(state=ud.name_surname)
async def answer_q2(message: types.Message, state: FSMContext):
    """Второй вопрос.
    Узнали имя пользователя.
    Просим рассказать в одном сообщении откуда он узнал о буткемпе"""
    name_surname = message.text

    await state.update_data(name_surname=name_surname)
    await message.answer(f"{st.CAME_FROM}" %name_surname, reply_markup=kb.main_menu)
    await ud.came_from.set()

@dp.message_handler(state=ud.came_from)
async def answer_q3(message: types.Message, state: FSMContext):
    """Третий вопрос.
    Просим ввести номер телефона"""
    user_name = message.from_user.first_name
    came_from = message.text

    await state.update_data(came_from=came_from)

    await message.answer(f"{st.TEL_NUMBER}" %user_name, reply_markup=kb.main_menu)
    await ud.tel_number.set()

@dp.message_handler(state=ud.tel_number)
async def answer_q4(message: types.Message, state: FSMContext):
    """Четвёртый вопрос.
    Просим ввести электронную почту"""
    # Достаем переменные
    # user_name = message.from_user.first_name
    tel_number, num = phone_checker(message.text)
    if num == 1:
        await state.update_data(tel_number=tel_number)
        await message.answer(f"{st.EMAIL}", reply_markup=kb.main_menu)
        await ud.email.set()
    else:
        await message.answer(st.TEL_ERROR, parse_mode='HTML')

@dp.message_handler(state=ud.email)
async def answer_q5(message: types.Message, state: FSMContext):
    """Последний вопрос. Просим подтвердить данные"""
    # Достаем переменные
    user_name = message.from_user.first_name
    email, num = email_checker(message.text)
    if num == 1:
        await state.update_data(email=email[0])
        l =['name_surname',
            'came_from',
            'tel_number',
            'email',
            'came_to']
        text = ''
        async with state.proxy() as data:
            text=st.CONFIRM_TEXT.format(*[data[i] for i in l])
            
        await message.answer(f"Спасибо, {user_name}!\nДавай подтвердим, что ты правильно всё заполнил: {text}", 
                            parse_mode='HTML', reply_markup=kb.booleanMenu)

        await ud.bool.set()
    else:
        await message.answer(st.EMAIL_ERROR, parse_mode='HTML')

@dp.message_handler(state=ud.bool)
async def answer_q6(message: types.Message, state: FSMContext):
    # Достаем переменные
    bool = message.text
    await state.update_data(bool=bool)
    await state.update_data(came_at_time=time.strftime('%X %x'))
    name = ''
    came_to = ''
    async with state.proxy() as data:
        name = name.join(data['name_surname'].split()[0])
        came_to = came_to.join(data['came_to'])

    l =[
        'name_surname',
        'user_id',
        'user_name',
        'came_at_time',
        'came_from',
        'tel_number',
        'email',
        'came_to'
    ]

    if bool == 'Да':
        await message.answer(st.MAP %name, parse_mode='HTML')
        async with state.proxy() as data:
            d = [data[i] for i in l]
            table.add_row(d)

            admin = {
                'DS': ds_admin,
                'JS': js_admin
                }
            
            try:
                await bot.send_message(chat_id = admin[came_to], text=d, parse_mode='HTML')
            except:
                logging.raiseExceptions('came_to is FALSE!')

        await state.finish()
        
    elif bool == 'Нет':
        await message.answer(st.NO_TEXT %name)
        await state.finish()

    else:
        pass

    await state.finish()
