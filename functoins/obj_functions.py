"""Содержит функции связанные с объектами(note): page_distribution и show_objects"""

from GUI import Note
from tkinter import Button, FLAT
from tkinter.messagebox import showwarning
from functoins.file_functions import loading
import os
import sys


def page_distribution(user_input='') -> list:
    """Возвращет вложенный спиок с
     распределенными объектами списока arr по сраницам
     (на одной странице 12 обектов)"""
    arr = os.listdir("resources/data")
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


def show_objects(root, arr: list, update_func):
    """Выводит обекты из списка arr на экран"""
    i = 0
    for file in arr:
        if file:
            try:
                note = Note(loading(file[:-5]), update_func)
                note.add_button(root).grid(row=i // 4, column=i % 4)
            except EOFError:
                os.remove(f"resources/data/{file}")  # удаляет этот файл
                showwarning(title="Преупреждение", message="Внимение\nОбнаружен чужеродный файл, для корректоной работы программа перезапустится")
                # перезапуск приложения
                python = sys.executable
                os.execl(python, python, *sys.argv)
        else:
            Button(root, relief=FLAT, width=20, height=10).grid(row=i // 4, column=i % 4)  # создание пустой кнопки
        i += 1
