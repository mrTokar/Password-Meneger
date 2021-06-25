"""Содержит функции связанные с объектами(note): page_distribution и show_objects"""

from Note import Note
from tkinter import Button, FLAT
from functoins.pickle_functions import loading
from os import listdir


def page_distribution(user_input=''):
    """возвращет вложенный спиок с
     распределенными объектами списока arr по сраницам
     (на одной странице 12 обектов)"""
    arr = listdir("data")
    page = 0
    obj_on_page = []
    while arr:
        obj_on_page.append([])
        i = 0
        while i != 12:
            if arr:
                item = arr.pop(0)
                if user_input.lower() in item.lower():
                    obj_on_page[page].append(item)
                    i += 1
            else:
                obj_on_page[page].append(None)
                i += 1
        page += 1
    return obj_on_page


def show_objects(root, arr):
    """выводит обекты из списка arr на экран"""
    i = 0
    for file in arr:
        if file is not None:
            note = Note(loading(file[:-5]))
            note.add_button(root).grid(row=i // 4, column=i % 4)
        else:
            Button(root, relief=FLAT, width=20, height=10).grid(row=i // 4, column=i % 4)
        i += 1
