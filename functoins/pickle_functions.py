'''Содержит функции связанные с библиотекой pickle: saving и loading'''
from pickle import dump, load


def saving(name, arr):
    # сохраняет информацию в именной файл
    dir = f"data/{name}.data"
    with open(dir, "wb") as file:
        dump(arr, file)


def loading(name):
    # загружает информацию из именного файла
    dir = f"data/{name}.data"
    with open(dir, "rb") as file:
        return load(file)
