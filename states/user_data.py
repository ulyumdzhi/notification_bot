# import collections
from aiogram.dispatcher.filters.state import State, StatesGroup

class UserData(StatesGroup):
    """Для хранения состояний.
    Наследуется от StatesGroup. Использует State."""
    name_surname = State()
    user_id = State()
    user_name_surname_from_tg = State()
    came_from = State()
    tel_number= State()
    email = State()
    came_to = State()
    came_at_time = State()
    bool = State()
    info = State()
    