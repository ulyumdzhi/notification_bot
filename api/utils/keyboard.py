from aiogram.types import ReplyKeyboardMarkup as RKM
from aiogram.types import KeyboardButton as KB

class ReplyTexts:
    def __init__(self):
        self.ds = 'DS'
        self.js = 'JS'
        self.howtofind = '/🗺 Как пройти?'
        self.iamhere = '/🚩 Я на месте!'
        self.repeat = 'Начать заново'
        self.yes = 'Да'
        self.no = 'Нет'
        self.agree = 'Даю согласие!'
        self.disagree = 'Не даю согласие!'
        
rt = ReplyTexts()

# Base buttons
btn_find = KB(rt.howtofind)
btn_here = KB(rt.iamhere)
btn_repeat= KB(rt.repeat)
btn_yes = KB(rt.yes)
btn_no = KB(rt.no)

# Hello menu
btn_agreed = KB(rt.agree)
btn_disagreed= KB(rt.disagree)
hello_menu = RKM(resize_keyboard=True, 
                one_time_keyboard=True)\
                .add(btn_disagreed, btn_repeat, btn_agreed)

# Q1 menu
btn_ds = KB(rt.ds)
btn_js = KB(rt.js)
dsjs_menu = RKM(resize_keyboard=True, 
            one_time_keyboard=True)\
            .add(btn_js, btn_repeat, btn_ds)

# Main menu
main_menu = RKM(resize_keyboard=True, 
            one_time_keyboard=True)\
            .add(btn_find, btn_repeat, btn_here)

# Bool Menu
booleanMenu = RKM(resize_keyboard=True, 
                one_time_keyboard=True)\
                .add(btn_no, btn_repeat, btn_yes)



