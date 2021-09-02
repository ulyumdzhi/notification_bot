from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class ReplyTexts:
    def __init__(self):
        self.ds = 'DS'
        self.js = 'JS'
        self.howtofind = '/🗺 Как пройти?'
        self.iamhere = '/🚩 Я на месте!'
        self.repeat = 'Начать заново'
        self.yes = 'Да'
        self.no = 'Нет'

RT = ReplyTexts()

btnRepeat= KeyboardButton(RT.repeat)

# Main Menu
btnDS = KeyboardButton(RT.ds)
btnJS = KeyboardButton(RT.js)

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, 
                                 one_time_keyboard=True).add(btnJS, btnDS)

# Bool Menu
btnYes = KeyboardButton(RT.yes)
btnNo = KeyboardButton(RT.no)
booleanMenu = ReplyKeyboardMarkup(resize_keyboard=True, 
                                 one_time_keyboard=True).add(btnNo, btnRepeat, btnYes)

# Second Menu
btnElbrus = KeyboardButton(RT.howtofind)
btnHere = KeyboardButton(RT.iamhere)

secondMenu = ReplyKeyboardMarkup(resize_keyboard=True, 
                                 one_time_keyboard=True).add(btnElbrus, btnRepeat, btnHere)



