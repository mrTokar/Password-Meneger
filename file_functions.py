"""Содержит функции связанные с работой с файлами: saving и loading, check_directory.
А также функцию распределющую объекты note по страницам - page_distribution"""
import os
from pickle import dump, load
from os import listdir, remove, mkdir, path, urandom
from PIL import Image
import sys
from hashlib import pbkdf2_hmac


def saving(arr: list, login: str):
    """Cохраняет информацию в именной файл"""
    directory = f"resources/data/{login}/{arr[0]}.data"
    with open(directory, "wb") as file:
        dump(arr, file)

def saving_hased_password(key: bytes, salt: bytes, login: str):
    """Сохраняет кортеж (key, salt) в папку ползователя"""
    directory = f"resources/__HASHEDPASSWORD__/__{login.upper()}__.data"
    try:
        with open(directory, "wb") as file:
            dump((key, salt), file)
        return None  # служит в качестве breake
    except FileNotFoundError:
        try:
            os.mkdir("resources/__HASHEDPASSWORD__")
        except FileNotFoundError:
            os.mkdir("resources")
            os.mkdir("resources/__HASHEDPASSWORD__")
    with open(directory, "wb") as file:
        dump((key, salt), file)


def loading(name: str, login: str) -> list:
    """Загружает информацию из именного файла"""
    directory = f"resources/data/{login}/{name}.data"
    with open(directory, "rb") as file:
        return load(file)


def loading_hashed_password(login: str) -> tuple:
    """Загружает key и salt. Если не находит дирректорию или фйл выводит showwaring"""
    directoty = f"resources/__HASHEDPASSWORD__/__{login.upper()}__.data"
    with open(directoty, "rb") as file:
      return load(file)
        

def check_image_file(dir_img: str):
    """Проверяет корректность загружаемой картинки. \n
    Если размер не соответствует 100х100, то удаляет ее."""
    img = Image.open(dir_img)
    if img.size != (100, 100):
        del img
        remove(dir_img)


def check_directory(directoty: str):
    """Проверяет наличие нужных файлов"""
    try:
        flag = True  # нет ни одного подходящего файла
        for file in listdir(f"resources/data/{directoty}"):
            if file[-5:] == '.data':
                flag = False  # уже есть хотя бы один подходящий файл
            else:
                remove(f"resources/data/{directoty}/{file}")  # удаляем не нужный файл
        if flag:  # если нет ни одного файла
            saving(["Example", "test@e-mail.com", "123456789", ""], directoty)
    except FileNotFoundError:  # если нет нужной дирректории
        try:
            mkdir(f"resources/data/{directoty}")
            saving(["Example", "test@e-mail.com", "123456789", ""], directoty)
        except FileNotFoundError:
            mkdir(f"resources/data")
            mkdir(f"resources/data/{directoty}")
            saving(["Example", "test@e-mail.com", "123456789", ""], directoty)


    try:  # проверка resources/images/login
        for file in listdir(f'resources/images/{directoty}'):
            if file[-4:] == '.png':
                check_image_file(f'resources/images/{directoty}/{file}')
            else:
                remove(f'resources/images/{directoty}/{file}')
    except FileNotFoundError:  # если нет нужной дирректории
        try:
            mkdir(f'resources/images/{directoty}')
        except FileNotFoundError:
            mkdir(f'resources/images')
            mkdir(f'resources/images/{directoty}')


def resource_path(relative_path: str):
    """Получает и возвращает абсолютный путь к ресурсу"""
    try:
        # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


def page_distribution(user_input: str, login: str) -> list:
    """Возвращет вложенный спиок с
     распределенными объектами списка arr по сраницам
     (на одной странице 12 обектов)"""
    arr = listdir(f"resources/data/{login}")
    page = 0
    obj_on_page = []
    while arr:
        obj_on_page.append([])
        i = 0
        while i != 12:
            if arr:
                item = arr.pop(0)
                if (user_input.lower() in item.lower()) and (item[-5:] == ".data"):
                    obj_on_page[page].append(item)
                    i += 1
            else:
                obj_on_page[page].append(None)
                i += 1
        page += 1
    return obj_on_page


def hash_password(password: str, salt=None):
    """Хеширует пароль и возвращает ключ с солью"""
    if not salt:
        salt = urandom(32)
    key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key, salt