"""Содержит функции связанные с библиотекой pickle: saving и loading"""
from pickle import dump, load


def saving(name, arr):
    # сохраняет информацию в именной файл
    directory = f"data/{name}.data"
    with open(directory, "wb") as file:
        dump(arr, file)


def loading(name):
    # загружает информацию из именного файла
    directory = f"data/{name}.data"
    with open(directory, "rb") as file:
        return load(file)
