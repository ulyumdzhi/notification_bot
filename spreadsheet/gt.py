
import logging
# from pprint import pprint

import httplib2
import googleapiclient.discovery as GACD
from oauth2client.service_account import ServiceAccountCredentials as SAC

from api.loader import CREDENTIALS_FILE, spreadsheet_id

class GoogleTable:
    """Необходимый функционал общения с таблицой Google Sheets."""
    def __init__(self, CREDENTIALS_FILE, spreadsheet_id, num_entries_to_read=100):
        # настройка связи с таблицей
        credentials = SAC.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets', 
            'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = GACD.build('sheets', 'v4', http = httpAuth)
        
        self.credentials = credentials
        self.spreadsheet_id = spreadsheet_id
        self.service = service
        self.range = 'A1:H%d' %num_entries_to_read

        self.raw_values = []

        # номера колонок в таблице
        self._name_surname = 0
        self._user_id = 1
        self._user_name = 2	
        self._came_at_time = 3
        self._came_from = 4
        self._tel_number = 5
        self._email = 6
        self._came_to = 7

        # параметры таблицы и данных
        self.columns = []
        self.data = [] 
        self.dict_data = {}
        self.entries_count = 0
        self.ds_num = 0
        self.js_num = 0

        self.update() 

        logging.info(f'Start entries_count {self.entries_count}')

    def update(self):
        """Актуализиурем данные в таблице."""
        values = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.range, 
            majorDimension='COLUMNS'
            ).execute()

        self.raw_values = values['values']

        self.columns = [col[0] for col in self.raw_values] # собираем названия колонок
        self.data = [col[1:] for col in self.raw_values] # срез по колонке без первого ряда названий
        self.dict_data = dict(zip(self.columns, self.data)) # собираем данные в словарь
        self.entries_count = len(self.dict_data[self.columns[self._user_id]]) # общее количество записей в таблице
        self.ds_num = sum([i=='DS' for i in self.dict_data[self.columns[self._came_to]]]) # количество записей Data Science
        self.js_num = sum([i=='JS' for i in self.dict_data[self.columns[self._came_to]]]) # количество записей JavaScript

    def add_row(self, data: str) -> bool:
        """Добавляем в таблицу массив ответов от пользователя"""
        self.update()

        logging.info(f'entries_count before new row {self.entries_count}')

        # Первая строка - это названия колонок, плюс ещё строка для новой записи. 
        # Итого нужно "добавить" 2 строки к entries_count, чтобы получить индекс строки
        # для новой записи от пользователя в таблицу 
        row_index = self.entries_count+2

        # запись данных в таблицу
        values = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"A{row_index}:H{row_index}",
                    "majorDimension": "ROWS",
                    "values": [[*data]]}
                ]
            }
        ).execute()

        self.update()
        logging.info(f'entries_count after new row {self.entries_count}')


table = GoogleTable(CREDENTIALS_FILE, spreadsheet_id)

