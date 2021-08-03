"""Содержит функции связанные с работой с файлами: saving и loading, check_directory.
А также функцию распределющую объекты note по страницам - page_distribution"""
from pickle import dump, load
from os import listdir, remove, mkdir, path
from PIL import Image
import sys


def saving(arr: list):
    """Cохраняет информацию в именной файл"""
    directory = f"resources/data/{arr[0]}.data"
    with open(directory, "wb") as file:
        dump(arr, file)


def loading(name: str) -> list:
    """Загружает информацию из именного файла"""
    directory = f"resources/data/{name}.data"
    with open(directory, "rb") as file:
        return load(file)


def check_image_file(dir_img: str):
    """Проверяет корректность загружаемой картинки. \n
    Если размер не соответствует 100х100, то удаляет ее."""
    img = Image.open(dir_img)
    if img.size != (100, 100):
        del img
        remove(dir_img)


def check_directory():
    """Проверяет наличие нужных файлов"""
    try:
        flag = True  # нет ни одного подходящего файла
        for file in listdir("resources/data"):
            if file[-5:] == '.data':
                flag = False  # уже есть хотя бы один подходящий файл
            else:
                remove(f"resources/data/{file}")  # удаляем не нужный файл
        if flag:  # если нет ни одного файла
            saving(["Example", "test@e-mail.com", "123456789", ""])
    except FileNotFoundError:  # если нет нужной дирректории
        mkdir("resources/data")
        saving(["Example", "test@e-mail.com", "123456789", ""])

    try:  # проверка resources/images
        for file in listdir('resources/images'):
            if file[-4:] == '.png':
                check_image_file(f'resources/images/{file}')
            else:
                remove(f'resources/images{file}')
    except FileNotFoundError:  # если нет нужной дирректории
        mkdir('resources/images')


def resource_path(relative_path: str):
    """Получает и возвращает абсолютный путь к ресурсу"""
    try:
        # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


def page_distribution(user_input='') -> list:
    """Возвращет вложенный спиок с
     распределенными объектами списка arr по сраницам
     (на одной странице 12 обектов)"""
    arr = listdir("resources/data")
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