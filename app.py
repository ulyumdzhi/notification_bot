from aiogram import executor
from api.dp import dp

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)