"""Содержит функции связанные с работой с файлами: saving и loading, check_directory"""
from pickle import dump, load
from os import listdir, remove, mkdir


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


def check_directory():
    """Проверяет наличие нужных файлов"""
    try:
        flag = True  # нет ни одного подходящего файла
        for file in listdir("resources/data"):
            if file[-5:] == '.data':
                flag = False # уже есть хотя бы один подходящий файл
            else:
                remove(f"resources/data/{file}") # удаляем не нужный файл
        if flag:  # если нет ни одного файла
            saving(["Example", "test@e-mail.com", "123456789", ""])
    except FileNotFoundError:  # если нет нужной дирректории
        mkdir("resources/data")
        saving(["Example", "test@e-mail.com", "123456789", ""])