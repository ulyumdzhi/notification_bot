import re
import time
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from api.loader import bot, dp, ds_admin, js_admin
from api.utils import static_text as st
from api.utils import keyboard as kb
from states.user_data import UserData as ud

@dp.message_handler(content_types=st.NOT_TARGET_CONTENT_TYPES)
async def not_target(message: types.Message):
    """Обрабатываем не текстовые сообщения"""
    user_name = message.from_user.first_name
    text = st.NOT_TARGET_TEXT %user_name
    await message.answer(text)


@dp.message_handler(Command("help"), state="*")
async def send_help(message: types.Message):
    """Обработка сообщения о помощи"""
    user_name = message.from_user.first_name
    user_fullname = message.from_user.full_name
    user_id = message.from_user.id   

    logging.info(f"Help alarm from id={user_id} named {user_fullname} at {time.strftime('%X %x')}")

    await message.answer(f"{st.HELP_TEXT}" %user_name, reply_markup=kb.main_menu)


@dp.message_handler(Command("start"), state="*")
async def send_welcome(message: types.Message):
    """Обработка стартового сообщения"""
    user_name = message.from_user.first_name
    user_fullname = message.from_user.full_name
    user_id = message.from_user.id   

    logging.info(f"Start massage from id={user_id} named {user_fullname} at {time.strftime('%X %x')}")

    await message.answer(f"{st.HELLO}" %user_name, reply_markup=kb.hello_menu)
    await ud.info.set()


@dp.message_handler(text='Начать заново', state="*")
async def restart(message: types.Message):
    """Обработка рестарта бота"""
    user_fullname = message.from_user.full_name
    user_id = message.from_user.id   

    logging.info(f"ReStart massage from id={user_id} named {user_fullname} at {time.strftime('%X %x')}")

    await send_welcome(message)


@dp.message_handler(state=ud.info)
async def answer_q0(message: types.Message, state: FSMContext):
    """Нулевой вопрос. 
    Согласие на обработку данных"""
    
    user_name = message.from_user.first_name
    user_fullname = message.from_user.full_name
    user_id = message.from_user.id    
    answer = message.text

    logging.info(f"from {user_name} permission {answer} at {time.strftime('%X %x')}")

    await state.update_data(info=answer)

    await message.answer(f"{st.INFO}", reply_markup=kb.dsjs_menu)

    await state.update_data(user_id=user_id)
    await state.update_data(user_name=user_fullname)
    await ud.came_to.set()


@dp.message_handler(text='Даю согласие!', state=ud.info)
async def restart(message: types.Message):
    """Обработка согласия бота"""

    await send_welcome(message)


@dp.message_handler(text='Не даю согласие!', state=ud.info)
async def restart(message: types.Message):
    """Обработка согласия бота"""

    await send_welcome(message)
    


    
