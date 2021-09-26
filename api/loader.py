import os
import time
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# вместо dotenv можно использовать config.py и подгружать все токены в виде статических переменных
from api.utils.config import * 

# Включаем логирование
logging.basicConfig(filename='log.log', 
                    encoding='utf-8',
                    level=logging.INFO)

# # Подгружаем переменные окружения, например из файла .env
load_dotenv()

# Telegram API токен @BotFather
try:
    TOKEN = BOT_TOKEN
except:
    TOKEN = os.getenv("BOT_TOKEN")

# Admin ID - те сотрудники, кому будут приходить оповещения, что гость уже на месте
try:
    ds_admin = DS_ADMIN_ID
    js_admin = JS_ADMIN_ID
except:
    ds_admin = os.getenv("DS_ADMIN_ID")
    js_admin = os.getenv("JS_ADMIN_ID")
    

# Инициализируем bot, dispatcher и storage
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=storage)

# Подгружаем данные для соединения с Google Sheets 
try:
    spreadsheet_id = TABLE_ID
except:
    spreadsheet_id = os.getenv("TABLE_ID")

CREDENTIALS_FILE = 'spreadsheet/credentials.json' # Google Developer Console 

logging.info(f"Start of bot at {time.strftime('%X %x')}")