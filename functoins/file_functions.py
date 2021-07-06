"""Содержит функции связанные с работой с файлами: saving и loading, check_directory"""
from pickle import dump, load
from os import listdir, remove, mkdir


def saving(arr:list):
    # сохраняет информацию в именной файл
    directory = f"data/{arr[0]}.data"
    with open(directory, "wb") as file:
        dump(arr, file)


def loading(name:str):
    # загружает информацию из именного файла
    directory = f"data/{name}.data"
    with open(directory, "rb") as file:
        return load(file)


def check_directory():
    # проверяет наличие нужных файлов
    try:
        true_files = []
        for file in listdir("data"):
            if file[-5:] == '.data':
                true_files.append(file)
            else:
                remove(f"data/{file}")
        if len(true_files) == 0:
            saving(["Example", "test@e-mail.com", "123456789", ""])
    except FileNotFoundError:
        mkdir("data")
        saving(["Example", "test@e-mail.com", "123456789", ""])