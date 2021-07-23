import os
import time
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# # вместо dotenv можно использовать config.py и подгружать все токены в виде статических переменных
# from config import * 

# Включаем логирование
logging.basicConfig(filename='log.log', 
                    encoding='utf-8',
                    level=logging.INFO)

# Подгружаем переменные окружения
load_dotenv()

# Telegram API токен @BotFather
TOKEN = os.getenv("BOT_TOKEN")

# Admin ID - те сотрудники, кому будут приходить оповещения, что гость уже на месте
ds_admin = os.getenv("DS_ADMIN_ID")
js_admin = os.getenv("JS_ADMIN_ID")

# Инициализируем bot, dispatcher и storage
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=storage)

# Подгружаем данные для соединения с Google Sheets 
spreadsheet_id = os.getenv("TABLE_ID")
CREDENTIALS_FILE = "notification_bot/spreadsheet/credentials.json" # Google Developer Console 

logging.info(f"Start of bot at {time.strftime('%X %x')}")




