from tkinter import Tk, X, RIGHT, BOTH, BOTTOM, Label
from tkinter.ttk import Frame, Entry
from functoins.obj_functions import page_distribution, show_objects
from Note import Buttons, Note


def __init__():
    """Создает настройки главного окна"""
    global master, entry, main_frame, button_frame, status, next_btn, back_btn
    # ============ переменные =============================
    global active_page, obj_on_page
    obj_on_page = page_distribution()
    active_page = 1  # активная страница

    master = Tk()
    master.title("Password Manager")
    master.iconbitmap("icon.ico")
    master.geometry(f"620x600+{master.winfo_screenwidth() // 2 - 310}+{master.winfo_screenheight() // 2 - 300}")
    master.resizable(False, False)

    # ============ виджеты поиска ========================
    search_frame = Frame(master)
    search_frame.pack(fill=X, padx=5, pady=5)

    entry = Entry(search_frame)
    entry.pack(fill=X, padx=5, expand=True)

    # ============ копки Найти и Добавить =================
    frame2 = Frame(master)  # рамка дял кнопок Найти и Добавить
    frame2.pack(fill=X)

    Buttons(frame2, text='Добавть', command=add_new).pack(side=RIGHT, padx=5, pady=5)

    Buttons(frame2, text='Найти', command=search).pack(side=RIGHT)

    # ========= виджеты результата поиска ==========
    main_frame = Frame(master)  # общая рамка для обектов и кнопок перелистывания
    main_frame.pack(fill=BOTH, expand=True)

    button_frame = Frame(main_frame)  # рамка для объектов
    button_frame.pack()

    status_frame = Frame(main_frame)  # рамка для отображения активной страницы и кнопок перемотки
    status_frame.pack(side=BOTTOM, padx=100, pady=5)

    next_btn = Buttons(status_frame, text="Далее >", command=page_up)
    next_btn.pack(side=RIGHT, padx=5)
    if active_page == len(obj_on_page):
        next_btn.disable()

    status = Label(status_frame, text=f"Стриница 1 из {len(obj_on_page)}")
    status.pack(sid=RIGHT)

    back_btn = Buttons(status_frame, text="< Назад", command=page_down)
    back_btn.pack(side=RIGHT, padx=5)
    back_btn.disable()


def add_new():
    """Добавляет новый обект"""
    new = Note(['', '', '', None])
    new.open_window(master=master)


def search(event=None):
    """выводит все объекты удовлетворяющий введеной строке в поле Entry\n
    event - своеобразная заглушка для привязки к Enter"""
    global active_page, obj_on_page, button_frame

    obj_on_page = page_distribution(user_input=entry.get())

    # =========== корректировка вывода =====================
    button_frame.destroy()
    button_frame = Frame(main_frame)
    button_frame.pack()
    show_objects(button_frame, obj_on_page[0])

    active_page = 1
    status.config(text=f"Страница {active_page} из {len(obj_on_page)}")
    back_btn.disable()  # кнопка назад
    if active_page == len(obj_on_page):  # кнопка далее
        next_btn.disable()
    else:
        next_btn.enable()


def page_up():
    """перелистывает на следующую страницу"""
    global active_page, obj_on_page, button_frame
    # ================= корректировка нижней строчки ==================
    active_page += 1
    status.config(text=f"Страница {active_page} из {len(obj_on_page)}")

    # кнопка далее
    if active_page == len(obj_on_page):
        next_btn.disable()
    else:
        next_btn.enable()

    back_btn.enable()  # кнопка назад
    button_frame.destroy()
    button_frame = Frame(main_frame)
    button_frame.pack()
    show_objects(button_frame, obj_on_page[active_page - 1])


def page_down():
    """перелистывает на страницу назад"""
    global active_page, obj_on_page, button_frame
    # ================= корректировка нижней строчки ==================
    active_page -= 1
    status.config(text=f"Страница {active_page} из {len(obj_on_page)}")

    next_btn.enable()  # кнопка далее
    # кнопка назад
    if active_page == 1:
        back_btn.disable()
    else:
        back_btn.enable()
    button_frame.destroy()
    button_frame = Frame(main_frame)
    button_frame.pack()
    show_objects(button_frame, obj_on_page[active_page - 1])


def main():
    __init__()

    # ========= создание всех кнопок ===================
    show_objects(button_frame, obj_on_page[0])

    # ========== запуск главного окна ===================
    master.bind("<Key>", search)
    master.mainloop()


if __name__ == "__main__":
    main()
