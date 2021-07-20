"""Содержит классы связанные с GUI приложения: Note, Window, ChildWindow, NoteWindow, Buttons"""

from tkinter import Tk, PhotoImage, X, LEFT, FLAT, Button, Entry, Label, Frame, BOTH, RAISED, RIGHT
from tkinter import Toplevel, W, Checkbutton, IntVar, Radiobutton, Scale, StringVar
from tkinter.constants import HORIZONTAL
from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename
from functoins.file_functions import saving
from os import remove
import pyperclip as ppc
from random import choice

state_past = False  # переменная состояния для корректного копирования в password_entry


class Buttons(Button):
    """Дочерний класс от класса Button. Имеет дополнительные аргументы:\n
    -disable отключает кнопку\n
    -enable включает кнопку"""

    def disable(self):
        """Выключает кнопку"""
        self.config(state="disable")

    def enable(self):
        """Включает кнопку"""
        self.config(state="normal")


class Window:
    """Класс главного окна"""

    def __init__(self, width: int, height: int, name="Password Manager"):
        self.master = Tk()
        self.master.title(name)
        self.master.iconbitmap("icon.ico")
        self.master.geometry(
            f"{width}x{height}+{self.master.winfo_screenwidth() // 2 - (width // 2)}+{self.master.winfo_screenheight() // 2 - (height // 2)}"
        )
        self.master.resizable(False, False)

    def run(self):
        """Открывает окно"""
        self.master.mainloop()


class ChildWindow:
    """Класс дочерних окон. Создает дочернее окно от аргумента parent.
    При инициализации имеет аргумент по умаолчанию name='Password Manager'
    Сразу установлены размеры окна и иконка. Фокусировка перелючается на данное окно.
    Автоматически создается 2 пространтсва: Освновное и для нижних кнопок.
    А также базовый кнопки: close_btn и ok_btn(без привязки к функциям!)"""

    def __init__(self, parent: Tk or Toplevel, width: int, height: int, name: str, resizeble: tuple):
        self.root = Toplevel(parent)
        self.root.title(name)
        self.root.iconbitmap("icon.ico")
        self.root.geometry(
            f"{width}x{height}+{self.root.winfo_screenwidth() // 2 - (width // 2)}+{self.root.winfo_screenheight() // 2 - (height // 2)}"
        )
        self.root.resizable(resizeble[0], resizeble[1])

        # основное пространство
        self.main_frame = Frame(self.root, relief=RAISED, borderwidth=1)
        self.main_frame.pack(fill=BOTH, expand=True)

        # простнранство всех нижних кнопок
        self.button_frame = Frame(self.root)
        self.button_frame.pack(fill=X, expand=False)
        Label(self.button_frame).pack(side=RIGHT, padx=70)  # заглушка чтобы кнопки были по середине

        self.close_btn = Buttons(self.button_frame, text="Закрыть")
        self.close_btn.pack(side=RIGHT, pady=10, padx=15)

        self.ok_btn = Buttons(self.button_frame, text="Ок", activebackground='#63DB64', )
        self.ok_btn.pack(side=RIGHT, padx=15)

    def grab_focus(self):
        """Захватывает фокус на создавшееся окно"""
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()


class NoteWindow(ChildWindow):
    """Дочерний класс от класса ChildWindow. Конфигупрация виджетов для Note"""

    def __init__(self, parent, width: int, height: int, name: str, resizeble=(False, True), **commands):
        ChildWindow.__init__(self, parent, width, height, name, resizeble)

        # Коррекитровка нижних кнопок
        self.del_btn = Buttons(self.button_frame, text='Удалить',
                               activebackground='red', command=commands['del_command'])  # кнопка Удалить
        self.del_btn.pack(anchor=W, padx=15, pady=10)

        self.ok_btn.config(text="Сохранить", command=commands['ok_command'])  # кнопка Сохранить

        self.close_btn.config(command=commands['close_command'])  # кнопка Закрыть

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
        self.name_entry = Entry(name_frame, font=('Andale Mono', 10))
        self.name_entry.pack(fill=X, padx=5, expand=True)

        # nickname
        nickname_frame = Frame(self.main_frame)
        nickname_frame.pack(fill=X)
        Label(nickname_frame, text="Nickname:", width=10).pack(side=LEFT, padx=5, pady=5)
        self.nickname_entry = Entry(nickname_frame, font=('Andale Mono', 10))
        self.nickname_entry.pack(fill=X, padx=5, expand=True)

        # password
        password_frame = Frame(self.main_frame)
        password_frame.pack(fill=X)
        Label(password_frame, text="Password:", width=10).pack(side=LEFT, padx=5, pady=5)
        self.password_entry = Entry(password_frame, font=('Andale Mono', 10))
        self.password_entry.pack(fill=X, padx=5, expand=True)

        # кнопка для генерации пароля
        Buttons(self.main_frame, text='Сгенерировать пароль', command=self.open_generate_window).pack()

    def open_generate_window(self):
        """Открывает окно с генерацией пароля"""
        global state_past
        GenerateWindow(self.root, 500, 300, "Generate Password")
        if state_past:
            self.password_entry.delete(0, 'end')
            self.password_entry.insert(0, ppc.paste())
            state_past = False

    def disable_del_button(self):
        """Оключает кнопку Удалить"""
        self.del_btn.disable()

    def get_name(self) -> str:
        """Возвращает текст из name_entry"""
        return self.name_entry.get()

    def get_nickname(self) -> str:
        """Возвращает текст из nickname_entry"""
        return self.nickname_entry.get()

    def get_password(self) -> str:
        """Возвращает текст из password_entry"""
        return self.password_entry.get()

    def get_dir_icon(self) -> str:
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


class GenerateWindow(ChildWindow):
    """Дочерний класс от класса ChildWindow. Конфигупрация виджетов для GeneratePassword"""

    def __init__(self, parent, width: int, height: int, name: str, resizeble=(False, False)):
        ChildWindow.__init__(self, parent, width, height, name, resizeble)

        # корректировка нижгних кнопок
        self.ok_btn.config(text="Скоприровать и сохранить", command=self.copy_and_save)
        self.close_btn.config(command=self.root.destroy)

        # области
        password_frame = Frame(self.main_frame)
        password_frame.pack(fill=X, expand=True)
        settings_frame = Frame(self.main_frame)
        settings_frame.pack(fill=X, expand=True, pady=10)

        # вывод пароля
        self.password = StringVar(value='')
        self.password_lbl = Label(password_frame, font=('Andale Mono', 12),
                                  width=35, height=2, bg='#DDDEDC', textvariable=self.password)
        self.password_lbl.pack(pady=25)

        # Настройки длинны пароля
        self.len_password = Scale(password_frame, length=150, orient=HORIZONTAL, from_=1, to=30, command=self.update)
        self.len_password.set(12)
        self.len_password.pack()

        # флажки
        flag_frame = Frame(settings_frame)
        flag_frame.pack(anchor=W, side=LEFT, expand=True, padx=15)

        self.variables = (('Lowercase', IntVar(value=1)), ('Uppercase', IntVar(value=1)),
                          ('Numbers', IntVar(value=1)), ('Symbols', IntVar(value=1)))
        self.checkbuttons = {}
        for name, variable in self.variables:
            self.checkbuttons[name] = Checkbutton(flag_frame, text=name, variable=variable, command=self.check_flag)
            self.checkbuttons[name].pack(anchor=W)

        # переключатели
        point_frame = Frame(settings_frame)
        point_frame.pack(anchor=W, side=LEFT, expand=True)

        self.point_choice = IntVar(value=0)
        Radiobutton(point_frame, text='Легкий для произношения', variable=self.point_choice, value=2,
                    command=self.radiobtn_easytosay_active).pack(anchor=W)
        Radiobutton(point_frame, text='Легкий для чтения', variable=self.point_choice, value=1,
                    command=self.radiobtn_easytoread_active).pack(anchor=W)
        Radiobutton(point_frame, text='Все символы', variable=self.point_choice, value=0,
                    command=self.radiobtn_all_chars_active).pack(anchor=W)

        self.update()
        self.grab_focus()

    def radiobtn_all_chars_active(self):
        """Выбирает и включает все флажки и генерирует новый пароль"""
        for name, variable in self.variables:
            check_btn = self.checkbuttons[name]
            check_btn.select()
            check_btn.config(state='normal')
        self.update()

    def radiobtn_easytosay_active(self):
        """Снимает метку и выключает флажки (Numbers, Symbols) и генерирует новый пароль"""
        for name, variable in self.variables:
            check_btn = self.checkbuttons[name]
            if name in ('Numbers', 'Symbols'):
                check_btn.deselect()
                check_btn.config(state='disable')
            else:
                check_btn.select()
                check_btn.config(state='normal')
        self.update()

    def radiobtn_easytoread_active(self):
        """Включает все флаги и генерирует новый пароль"""
        for name, variable in self.variables:
            check_btn = self.checkbuttons[name]
            check_btn.config(state='normal')
        self.update()

    def check_flag(self):
        """Проверяет корректность флагов.
        \n Если пользователь выключает последний флаг, то он заново включается"""
        info = []
        for name, variable in self.variables:
            info.append(variable.get())
        if not any(info):
            self.checkbuttons['Lowercase'].select()
        self.update()

    def update(self, val=None):
        """Обновляет password_label c новым случайно сгенерированным паролем.
        Аргумент val не требует передачи какого-либо значения и являяется заглушкой."""
        password = ''
        all_chars = {"Lowercase": tuple(range(97, 122)),
                     "Uppercase": tuple(range(65, 90)),
                     "Numbers": tuple(range(48, 57)),
                     "Symbols": (33, 35, 36, 37, 38, 42, 64, 94)}
        using_chars = []

        # определение возможных символов
        for name, variable in self.variables:
            if variable.get():
                using_chars.append(all_chars[name])

        # составление исключений
        if self.point_choice.get() == 1:
            ignore = 'O0Il1'
        else:
            ignore = ''

        # генерация пароля
        while len(password) != self.len_password.get():
            char = chr(choice(choice(using_chars)))
            if char not in ignore:
                password += char

        self.password.set(password)

    def copy_and_save(self):
        """Добавляет сгенерированный пароль в буфер обмена и закрывает окно"""
        global state_past
        ppc.copy(self.password.get())
        state_past = True
        self.root.destroy()


class Note:
    """Класс обектов содержащих все записи. Имеет методы для создания окна содержащего всю информацию
    и для добавления кнопки этой записи на главное окошко"""

    def __init__(self, arr: list, update_func):
        """инициализации объекта \n
         arr - спиок [name, nickname, password, icon] \n
         update_func - ссылка на функцию searh()"""
        self.name = arr[0]
        self.nickname = arr[1]
        self.password = arr[2]
        self.icon = None
        self.disable_del = False
        self.update_func = update_func

    def add_button(self, master: Tk) -> Buttons:
        """Добавляет инонку записи в окно. И возвращает данную кнопку"""
        self.master = master
        formed_name = self.formatted_name()
        img = PhotoImage(file=self.icon) if self.icon is not None else None
        btn = Buttons(master, text=formed_name, activebackground="#CCCCCC", relief=FLAT,
                      width=20, height=10, command=self.open_window)
        return btn

    def open_window(self, master=None):
        """Открывает окно данной записки.\n
        Аргумент master нужен для функции add_new(), т.к. она не вызывает аргумент add_button"""
        if master:
            self.password_window = NoteWindow(master, 500, 250, self.name, del_command=self.del_note,
                                              ok_command=self.save_note, close_command=self.close_note,
                                              choose_command=self.choose_icon)
        else:
            self.password_window = NoteWindow(self.master, 500, 250, self.name, del_command=self.del_note,
                                              ok_command=self.save_note, close_command=self.close_note,
                                              choose_command=self.choose_icon)

        if master or self.disable_del:
            # если объект новый, то удалить его нельзя
            self.password_window.disable_del_button()
            self.disable_del = False

        self.password_window.insert_text(name=self.name, nickname=self.nickname, password=self.password)

        self.password_window.grab_focus()  # запуск

    def formatted_name(self) -> str:
        """Форматирует Note.name для корректного изображения на кнопке"""
        len_string = 0
        name = ''
        last_word = self.name.split()[-1]
        for word in self.name.split()[:-1]:
            len_string += len(word)
            if len_string <= 20:
                name += word + ' '
            else:
                len_string = len(word)
                name += '\n' + word + ' '

        if len(last_word) <= 20:
            # если слово помещается целиком в 1 строку
            len_string += len(last_word)
            if len_string <= 20:
                name += last_word
            else:
                len_string = len(last_word)
                name += '\n' + last_word
        else:
            # инче каждый символ записываем поочереди и переносим строку когда та кончается
            for symbol in last_word:
                len_string += 1
                if len_string <= 20:
                    name += symbol
                else:
                    name += '\n' + symbol
                    len_string = 1

        return name

    def save_note(self):
        """Сохраняет данные"""
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
        self.update_func()

    def choose_icon(self):
        """Открывает диалоговое окно для выбора файла"""
        root = Tk()
        root.iconbitmap("icon.ico")
        root.withdraw()
        self.icon = askopenfilename()

    def del_note(self):
        """Вызывает уточняющий messagebox и удаляет записку при потвержении."""
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
            self.update_func()

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
                self.update_func()