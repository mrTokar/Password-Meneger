"""Содержит классы Note и Buttons"""

from tkinter import Tk, PhotoImage, X, LEFT, FLAT, Button, Entry, Label, Frame, BOTH, RAISED, RIGHT
from tkinter import Toplevel, W
from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename
from functoins.file_functions import saving
from os import remove


class Window:
    """Класс главного окна"""


    def __init__(self, width:int, height:int, name="Password Manager"):
        self.master = Tk()
        self.master.title(name)
        self.master.iconbitmap("icon.ico")
        self.master.geometry(
            f"{width}x{height}+{self.master.winfo_screenwidth() // 2 - (width//2)}+{self.master.winfo_screenheight() // 2 - (height//2)}"
        )
        self.master.resizable(False, False)


    def run(self):
        "Открывает окно"
        self.master.mainloop()


class ChildWindow:
    """Класс дочерних окон. Создает дочернее окно от аргумента parent.
    При инициализации имеет аргумент по умаолчанию name='Password Manager'
    Сразу установлены размеры окна и иконка. Фокусировка перелючается на данное окно.
    Автоматически создается 2 пространтсва: Освновное и для нижних кнопок.
    А также базовый кнопки (без привязки к функциям!)"""
    def __init__(self, parent, width:int, height:int, name:str, resizeble:tuple):
        self.root = Toplevel(parent)
        self.root.title(name)
        self.root.iconbitmap("icon.ico")
        self.root.geometry(
            f"{width}x{height}+{self.root.winfo_screenwidth() // 2 - (width//2)}+{self.root.winfo_screenheight() // 2 - (height//2)}"
        )
        self.root.resizable(resizeble[0], resizeble[1])

        # основное пространство
        self.main_frame = Frame(self.root, relief=RAISED, borderwidth=1)
        self.main_frame.pack(fill=BOTH, expand=True)

        # простнранство всех нижних кнопок
        self.button_frame = Frame(self.root)
        self.button_frame.pack(fill=X, expand=False)
        Label(self.button_frame).pack(side=RIGHT, padx=70) # заглушка чтобы кнопки были по середине

        self.close_btn = Buttons(self.button_frame, text="Закрыть")
        self.close_btn.pack(side=RIGHT, pady=10)

        self.ok_btn = Buttons(self.button_frame, text="Ок", activebackground='#63DB64',)
        self.ok_btn.pack(side=RIGHT, padx=15)


    def grab_focus(self):
        """Захватывает фокус на создавшееся окно"""
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()


class NoteWindow(ChildWindow):
    """Дочерний класс от класса ChildWindow. Конфигупрация виджетов для Note"""
    def __init__(self, parent, width:int, height:int, name:str, resizeble=(False, True), **commands):
        ChildWindow.__init__(self, parent, width, height, name, resizeble)

        # Коррекитровка нижних кнопок
        self.del_btn = Buttons(self.button_frame, text='Удалить',
                               activebackground='red', command=commands['del_command']) # кнопка Удалить
        self.del_btn.pack(anchor=W, padx = 15, pady=10)

        self.ok_btn.config(text="Сохранить", command=commands['ok_command']) # кнопка Сохранить

        self.close_btn.config(command=commands['close_command']) # кнопка Закрыть

        # иконка и ее выбор
        icon_frame = Frame(self.main_frame)
        icon_frame.pack(fill=X, pady=10, padx=50)

        self.image_lbl = Label(icon_frame)
        self.image_lbl.pack(side=LEFT, expand=True)
        Button(icon_frame, text="Выбрать иконку...", command=commands['choose_command']).pack(expand=True, side=LEFT)

        # название
        name_frame = Frame(self.main_frame)
        name_frame.pack(fill=X)
        Label(name_frame, text="Name:", width=10).pack(side=LEFT, padx=5, pady=5)
        self.name_entry = Entry(name_frame)
        self.name_entry.pack(fill=X, padx=5, expand=True)

        # nickname
        nickname_frame = Frame(self.main_frame)
        nickname_frame.pack(fill=X)
        Label(nickname_frame, text="Nickname:", width=10).pack(side=LEFT, padx=5, pady=5)
        self.nickname_entry = Entry(nickname_frame)
        self.nickname_entry.pack(fill=X, padx=5, expand=True)

        # password
        password_frame = Frame(self.main_frame)
        password_frame.pack(fill=X)
        Label(password_frame, text="Password:", width=10).pack(side=LEFT, padx=5, pady=5)
        self.password_entry = Entry(password_frame)
        self.password_entry.pack(fill=X, padx=5, expand=True)


    def disable_del_button(self):
        """Оключает кнопку Удалить"""
        self.del_btn.disable()


    def get_name(self):
        """Возвращает текст из name_entry"""
        return self.name_entry.get()


    def get_nickname(self):
        """Возвращает текст из nickname_entry"""
        return self.nickname_entry.get()


    def get_password(self):
        """Возвращает текст из password_entry"""
        return self.password_entry.get()


    def get_dir_icon(self):
        """Возвращает путь к иконке"""
        pass


    def insert_text(self, **messages):
        """Вставляет текст в указанные Entry"""
        try:
            self.name_entry.insert(0, messages['name'])
        except KeyError:
            pass

        try:
            self.nickname_entry.insert(0, messages['nickname'])
        except KeyError:
            pass

        try:
            self.password_entry.insert(0, messages['password'])
        except KeyError:
            pass


    def close_window(self):
        """Закрывает окно"""
        self.root.destroy()


class Note:
    """Класс обектов содержащих все записи. Имеет методы для создания окна содержащего всю информацию
    и для добавления кнопки этой записи на главное окошко"""

    def __init__(self, arr):
        """ функция инициализации объекта
         arr - спиок [name, nickname, password, icon]"""
        self.name = arr[0]
        self.nickname = arr[1]
        self.password = arr[2]
        self.icon = None
        self.disable_del = False

    def add_button(self, master):
        """добавляет инонку записи"""
        self.master = master
        img = PhotoImage(file=self.icon) if self.icon is not None else None
        btn = Button(master, text=self.name, activebackground="#CCCCCC", relief=FLAT,
                     width=20, height=10, command=self.open_window)
        return btn

    def open_window(self, master=None):
        """Открывает окно данной записки\n
        аргумент master нужен для функции add_new(), т.к. она не вызывает аргумент add_button"""
        if master:
            self.password_window = NoteWindow(master, 500, 200, self.name, del_command=self.del_note,
                                              ok_command=self.save_note, close_command=self.close_note,
                                              choose_command=self.choose_icon)
        else:
            self.password_window = NoteWindow(self.master, 500, 200, self.name, del_command=self.del_note,
                                              ok_command=self.save_note, close_command=self.close_note,
                                              choose_command=self.choose_icon)

        if master or self.disable_del:  # если объект новый, то удалить его нельзя
            self.password_window.disable_del_button()
            self.disable_del = False

        self.password_window.insert_text(name=self.name, nickname=self.nickname, password=self.password)

        self.password_window.grab_focus() # запуск


    def save_note(self):
        """сохраняет данные"""
        if self.name != self.password_window.get_name():
            try:
                remove(f"data/{self.name}.data")
                self.name = self.password_window.get_name()
            except FileNotFoundError:
                self.name = self.password_window.get_name()
        self.nickname = self.password_window.get_nickname()
        self.password = self.password_window.get_password()
        self.icon = self.password_window.get_dir_icon()
        saving([self.name, self.nickname, self.password, self.icon])
        self.password_window.close_window()


    def choose_icon(self):
        """открывает диалоговое окно для выбора файла"""
        root = Tk()
        root.iconbitmap("icon.ico")
        root.withdraw()
        self.icon = askopenfilename()

    def del_note(self):
        """Вызывает уточняющий messagebox и удаляет записку."""
        answer = askyesno(title="Потверждение удаления",
                          message=f"Вы действительно хотите безвозратно удалить пароль от {self.name}?")
        if answer:
            remove(f"data/{self.name}.data")
            self.name = ''
            self.nickname = ''
            self.password = ''
            self.icon = None
            self.disable_del = True
            self.password_window.close_window()

    def close_note(self):
        """Вызывает уточняющий messagebox если новые изменения не сохранены."""
        check_name = self.name == self.password_window.get_name()
        check_nickname = self.nickname == self.password_window.get_nickname()
        check_password = self.password == self.password_window.get_password()
        if check_name and check_nickname and check_password:
            self.password_window.close_window()
        else:
            answer = askyesno(title="Потверждение выхода",
                              message="Вы не сохранили последние изменения.\n           Вы точно хотите выйти?")
            if answer:
                self.password_window.close_window()


class Buttons(Button):
    """Дочерний класс от класса Button. Имеет дополнительные аргументы:\n
    -disable отключает кнопку\n
    -enable включает кнопку"""

    def disable(self):
        # выключает кнопку
        self.config(state="disable")

    def enable(self):
        # включает кнопку
        self.config(state="normal")


def print_kek():
    print("kek")


if __name__ == "__main__":
    root = Window(200,100)
    NoteWindow(root.master, 500, 200, "KEK", del_command=print_kek, ok_command=print_kek, close_command=print_kek, choose_command=print_kek)
    root.run()
