import os
import sqlite3
from win32api import SetFileAttributes
from win32con import FILE_ATTRIBUTE_HIDDEN

class LoginError(Exception):
    """Исключение LoginError поднимаетсся, если в БД не существует нужной улючевой ячейки"""
    def __init__(self, login = ""):
        if login:
            self.message = f"User's name '{login}' does not exist"
        else:
            self.message = "This User does not exist"

    def __str__(self):
        return self.message

class DB:

    def __init__(self, table: str):
        """table - нужная таблица (пользователь)"""
        if os.path.isdir('resources'): 
            "Если в данной дирректории есть папка resources"

            if "data.db" not in os.listdir("resources"):
                file = open("resources\\data.db", "w+")
                file.close()
        else:
            os.mkdir("resources")
            file = open("resources\\data.db", "w+")
            file.close()
        SetFileAttributes("resources\\data.db", FILE_ATTRIBUTE_HIDDEN)

        self.connect_db()
        self.table = table
        self.check_table()

    def get_table(self):
        """Возвращает назвавние подключенной таблицы"""
        return self.table

    def connect_db(self):
        "Подключение к БД"

        self.connection = sqlite3.connect("resources\\data.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def connection_close(self):
        "Отключение от БД"

        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
    
    def check_connection(self) -> bool:
        "Проверка соединения"

        if self.cursor is not None:
            if self.connection is not None:
                return True

    def check_table(self):
        """Проверка существования таблицы. В случае отсутвия создает ее."""

        try:
            self.cursor.execute('SELECT * FROM {self.table}')
        except sqlite3.OperationalError:
            self.create_new_table()

    def load(self, key: str) -> list:
        """Загрузка информации из бд по ключу key.
        Возвращает список [name, nickname, password, icon] \n
        key - ключ, по каторому нужно загрузить информацию"""
               
        self.cursor.execute('SELECT * FROM {}'.format(self.table))
        rows = self.cursor.fetchall()

        for note in rows:
            if note[0] == key:
                return list(map(str, note))

    def load_all_name(self, filter='') -> list:
        """Возвращает все запис включяющие в себя фильтр из таблицы нужной таблицы. \n
        filter - фильр, по котром производиться поиск"""
        filter= filter.lower()
        self.cursor.execute('SELECT * FROM {}'.format(self.table))
        rows = self.cursor.fetchall()
        arr = [note[0] for note in rows if filter in note[0].lower()]
        obj_on_page = []
        for page in range(len(arr)//12 + 1): 
            obj_on_page.append([])
            for _ in range(12):
                if arr:
                    obj_on_page[page].append(arr.pop(0))
                    continue
                obj_on_page[page].append(None)
        return obj_on_page

    def save(self, arr: list):
        """Сохранение списка arr [name, nickname, password, icon].
        Каждый эдлемент соответственно в свое поле БД. \n
        arr - сохраняемый список"""
        
        info_cells = list(self.cursor.execute("PRAGMA table_info({});".format(self.table)))
        keys =[]
        for i in info_cells:
            keys.append(i[1])
        keys = ", ".join(keys)

        string = lambda x: '"' + x + '"' if x is not None else '"default"'
        vaules = ', '.join(list(map(string, arr)))
        
        operation = (f'INSERT or REPLACE into {self.table} ({keys}) VALUES ({vaules})')
        self.cursor.execute(operation)
        self.connection.commit()

    def create_new_table(self):
        """Создание новой таблицы в БД"""

        if self.check_connection():
            len_cells = 4
            name_of_cells = ['name', 'nickname', 'password', 'icon']
            key = 0
            cells = ''

            for i in range(len_cells):
                if key == i:
                    cell = f'{name_of_cells[i]} string PRIMARY KEY, '
                else:
                    cell = f'{name_of_cells[i]} string, '
                cells += cell
            cells = cells.rstrip(cells[-1])
            cells = cells.rstrip(cells[-1])
            try:
                self.cursor.execute(f'CREATE TABLE {self.table}({cells})')
                self.connection.commit()
                self.save(["Example", "test2020@gmail.com", "123456789", "default"])
            except sqlite3.OperationalError:
                pass

        else:
            self.connect_db()
            self.create_new_table(self.table)


    def delete_note(self, key: str):
        """Удаление строчки по заначению key в стобце name из таблицы login в БД. \n
        key - значение в ячейке name (ключ по котрой будет удалена строчка)"""

        self.cursor.execute("DELETE FROM {0} WHERE {1} = '{2}'".format(self.table, "name", key))
        self.connection.commit()

    
    def delete_table(self, login: str):
        """Полное удаление всей таблицы(пользователя). \n
        login - нужная таблица"""
	
        self.cursor.execute('DELETE FROM {}'.format(login))
        self.connection.commit()
        self.connection_close()


class DB_hash:

    def __init__(self):
        if os.path.isdir('resources'): 
            "Если в данной дирректории есть папка resources"

            if "hashedpasswords.db" not in os.listdir("resources"):
                file = open("resources\\hashedpasswords.db", "w+")
                file.close()
        else:
            os.mkdir("resources")
            file = open("resources\\hashedpasswords.db", "w+")
            file.close()
        SetFileAttributes("resources\\hashedpasswords.db", FILE_ATTRIBUTE_HIDDEN)

        self.connect_db()
        self.check_table()

    def connect_db(self):
        "Подключение к БД"

        self.connection = sqlite3.connect("resources\\hashedpasswords.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def connection_close(self):
        "Отключение от БД"

        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
    
    def check_connection(self) -> bool:
        "Проверка соединения"

        if self.cursor is not None:
            if self.connection is not None:
                return True

    def saving(self, login: str, key: str, salt: str, color: str):
        """Cохраняет новго пользоваетля \n
        login - нужный пользователь \n
        key - сохраняемый ключ \n
        salt - сохраняемая соль \n
        color - ответ на спец вопрос"""

        color = color.strip().lower()  # подгонка под один стиль
        info_cells = list(self.cursor.execute("PRAGMA table_info(hash);"))
        keys =[]
        for i in info_cells:
            keys.append(i[1])
        keys = ", ".join(keys)

        vaules = f"\"{login}\", \"{str(key)}\", \"{str(salt)}\", \"{color}\""
        
        operation = (f'INSERT or REPLACE into hash ({keys}) VALUES ({vaules})')
        self.cursor.execute(operation)
        self.connection.commit()

    def load(self, login: str) -> tuple:
        """Возвращает данные о пользователе из БД.\n
        login - нужный пользователь, по котрому нужно загрузить кортеж"""

        self.cursor.execute('SELECT * FROM hash')
        rows = self.cursor.fetchall()
        if rows is None:
            raise LoginError(login)
        for note in rows:
            if note[0] == login:
                return note
        raise LoginError(login)

    def create_new_table(self):
        """Создание таблицы в БД (в случае ее отсутствия)"""

        if self.check_connection():

            len_cells = 4
            name_of_cells = ['login', 'key', 'salt', 'color']
            key = 0
            cells = ''

            for i in range(len_cells):
                if key == i:
                    cell = f'{name_of_cells[i]} string PRIMARY KEY, '
                else:
                    cell = f'{name_of_cells[i]} string, '
                cells += cell
            cells = cells.rstrip(cells[-1])
            cells = cells.rstrip(cells[-1])
            try:
                self.cursor.execute(f'CREATE TABLE hash({cells})')
            except sqlite3.OperationalError:
                pass

            self.connection.commit()

    def check_table(self):
        """Проверка существования таблицы. В случае отсутвия создает ее."""

        try:
            self.cursor.execute('SELECT * FROM hash')
        except sqlite3.OperationalError:
            self.create_new_table()
    

    def delete_note(self, login: str):
        """Удаление входных данных пользователя в БД. \n
        login - нужный пользователь"""

        self.cursor.execute("DELETE FROM {0} WHERE {1} = '{2}'".format('hash', 'login', login))
        self.connection.commit()


if __name__ == "__main__":
    test2 = DB_hash()
    test2.saving("tokar", bytes('10101100', encoding='utf-8').hex(), bytes('100110110', encoding='utf-8').hex(), "green")
    print(test2.load('tokar'))
    test2.saving("tokar", bytes('10101100', encoding='utf-8').hex(), bytes('100110110', encoding='utf-8').hex(), "red")
    print(test2.load('tokar'))