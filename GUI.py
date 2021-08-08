"""Содержит классы связанные с GUI приложения: Note, Window, ChildWindow, NoteWindow, Buttons"""

from tkinter import TclError, Tk, Button, Entry, Label, Frame
from tkinter import Toplevel, Checkbutton, IntVar, Radiobutton, Scale, StringVar
from tkinter.constants import END, INSERT, SEL_FIRST, SEL_LAST, TOP, HORIZONTAL, LEFT, X, RIGHT, RAISED, BOTH, W, FLAT, BOTTOM, GROOVE
from tkinter.messagebox import askyesno, showwarning
from tkinter.filedialog import askopenfilename
from win32api import GetKeyboardLayout, LoadKeyboardLayout
from PIL import Image as PilImage
from PIL import ImageTk
from random import choice
import file_functions as func
import pyperclip as ppc
import os
import sys

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
    """Класс окна. (Трофарет)"""

    def __init__(self, width: int, height: int, name):
        self.master = Tk()
        self.master.title(name)
        self.master.iconbitmap(func.resource_path("resources/icon.ico"))
        self.master.geometry(
            f"{width}x{height}+{self.master.winfo_screenwidth() // 2 - (width // 2)}+{self.master.winfo_screenheight() // 2 - (height // 2)}"
        )
        self.master.resizable(False, False)
        self.first = True

    def set_eng(self, event):
        """Устанавливает Англискую раскладку только один раз при активации окна"""
        if self.first :
            LoadKeyboardLayout('00000409', 1)
            self.first = False

    def copy_rus(self, event):
        """Функция копирования. Активируется Ctrl+С"""
        if isinstance(event.widget, Entry) and hex(GetKeyboardLayout()) != "0x4090409":
            try:
                ppc.copy(event.widget.selection_get())
            except TclError:
                pass

    def selectall_rus(self, event):
        """Функция выделения всего. Активируется Ctrl+Ф"""
        if isinstance(event.widget, Entry) and hex(GetKeyboardLayout()) != "0x4090409":
            self.master.after(10, lambda w: w.selection_range(0, END), event.widget)
            event.widget.icursor(END)

    def past_rus(self, event):
        """Функция вставления текста. Активируется Ctrl+М"""
        if isinstance(event.widget, Entry) and hex(GetKeyboardLayout()) != "0x4090409":
            try:
                event.widget.delete(SEL_FIRST, SEL_LAST)
                event.widget.insert(INSERT, ppc.paste())
            except TclError:
                event.widget.insert(INSERT, ppc.paste())

    def cut_rus(self, event):
        """Функция вырезки текста. Активируется Ctrl+Ч"""
        if isinstance(event.widget, Entry) and hex(GetKeyboardLayout()) != "0x4090409":
            try:
                ppc.copy(event.widget.selection_get())
                event.widget.delete(SEL_FIRST, SEL_LAST)
            except TclError:
                pass

    def run(self):
        """Открывает окно"""
        self.master.mainloop()
        self.set_eng(None)


class LoginWindow(Window):
    """Окно входа. Просит ввести пароль прежде чем показать пароли."""
    def __init__(self):
        super().__init__(500, 300, "Войдите в учётную запись")
        # основное пространство
        main_frame = Frame(self.master, relief=RAISED, borderwidth=1)
        main_frame.pack(fill=BOTH, expand=True)

        # простнранство всех нижних кнопок
        self.button_frame = Frame(self.master)
        self.button_frame.pack(fill=X, expand=False)
        Label(self.button_frame).pack(side=RIGHT, padx=70)  # заглушка чтобы кнопки были по середине

        self.login_btn = Buttons(self.button_frame, text="Вход", command=self.log_in)
        self.login_btn.pack(side=RIGHT, pady=10, padx=15)

        self.create_btn = Buttons(self.button_frame, text="Создать новый аккаунт", command=self.create_new)
        self.create_btn.pack(side=RIGHT, padx=15)

        Label(main_frame, text="Password Manager", font=('Arial', 24)).pack()
        Label(main_frame, text="Авторизуйтесь").pack(pady=20)
        login_frame = Frame(main_frame)
        login_frame.pack(padx=20)

        Label(login_frame, text="Логин:").pack(anchor=W)
        self.login_entry = Entry(login_frame, font=("Andale Mono", 10))
        self.login_entry.pack(fill=X, anchor=W)

        Label(login_frame, text="Пароль:").pack(anchor=W)
        self.password_entry = Entry(login_frame, font=("Andale Mono", 10), show="*")
        self.password_entry.pack(fill=X, anchor=W)

        self.master.protocol("WM_DELETE_WINDOW", self.stop_program)
        self.master.bind("<Return>", self.log_in)
        self.master.bind("<Key>", self.on_bind)  # подключение горячик клавиш

    def create_new(self):
        """Создает новый аккунт, по данным из полей ввода."""
        self.login = self.login_entry.get()
        if self.login != '' and \
                self.password_entry.get() != '':  # если заполены все поля ввода
            key, salt = func.hash_password(self.password_entry.get())  # хеширование введенного пароля  
            func.saving_hased_password(key, salt, self.login)  # сохранение ключа и соли
            self.master.destroy()  # выходим из этого окна
        else:  # иначне выходим выводим предупреждение о том что заполнены не все поля 
            showwarning(title="Внимание", message="Оба поля ввода должны быть заполнены")

    def log_in(self, event=None):
        """Проверяет корректность пароля.
        event - заглушка для првязки к нажатию Enter"""
        self.login = self.login_entry.get()  # получает логин
        if self.login != '' and self.password_entry.get() != '':  # если введено все поля ввода
            try:  # пытаемся загрузить ключ и сольь
                true_key, salt = func.loading_hashed_password(self.login)  # загрузка из памяти ключа и соли
                new_key, salt = func.hash_password(self.password_entry.get(), salt)  # хеширование введнного пароля по загруженной соли 
                if new_key == true_key:  # если введен паравильный пароль
                    self.master.destroy()  # выходим из этого окна
                else:  # иначе выводим предупреждение о том что неверный пароль
                    showwarning(title="Внимание", message="Неверный пароль")
            except FileNotFoundError:
                showwarning(title="Внимание", message="Пользователь не найден")
        else:  # иначе выводим предупреждение о том что заполенены не все поля ввода 
            showwarning(title="Внимание", message="Оба поля ввода должны быть заполнены")

    def get_login(self):
        """Возвращает login (папку где сохранены парли пользоваетеля)"""
        return self.login

    def stop_program(self):
        """Останавливает программу, при закрытии окна"""
        sys.exit(0)

    def on_bind(self, event):
        """Вызывается при нажатии любой клавиши. Если это горячие сочетания,
         то вызывает эту функцию."""
        if (event.state & 4 > 0):
            symbol = chr(event.keycode)
            if symbol == "A":
                self.selectall_rus(event)
            elif symbol == "X":
                self.cut_rus(event)
            elif symbol == "C":
                self.copy_rus(event)
            elif symbol == "V":
                self.past_rus(event)


class MainWindow(Window):
    """Класс главного окна."""
    def __init__(self, login):
        """login - папка пользователя"""
        self.login = login
        super().__init__(620, 610, "Password Manager")
        self.obj_on_page = func.page_distribution('', self.login)
        self.active_page = 1  # активная страница

        # ============ виджеты поиска ========================
        search_frame = Frame(self.master)
        search_frame.pack(fill=X, padx=5, pady=15)

        self.entry = Entry(search_frame, fg="grey")
        self.entry.insert(0, "Поиск...")
        self.entry.pack(fill=X, padx=5, expand=True)

        # ============ копка Добавить =================
        frame2 = Frame(self.master)  # рамка для кнопоки Добавить
        frame2.pack(fill=X)

        Buttons(frame2, text='Добавить новый пароль', relief=GROOVE,
                command=self.add_new).pack(padx=5, pady=5, fill=X)

        # ========= виджеты результата поиска ==========
        self.main_frame = Frame(self.master)  # общая рамка для обектов и кнопок перелистывания
        self.main_frame.pack(fill=BOTH, expand=True)

        self.button_frame = Frame(self.main_frame)  # рамка для объектов
        self.button_frame.pack()

        status_frame = Frame(self.main_frame)  # рамка для отображения активной страницы и кнопок перемотки
        status_frame.pack(side=BOTTOM, padx=100, pady=5)

        self.next_btn = Buttons(status_frame, text="Далее >", command=self.page_up)
        self.next_btn.pack(side=RIGHT, padx=5)
        if self.active_page == len(self.obj_on_page):
            self.next_btn.disable()

        self.status = Label(status_frame, text=f"Стриница 1 из {len(self.obj_on_page)}")
        self.status.pack(sid=RIGHT)

        self.back_btn = Buttons(status_frame, text="< Назад", command=self.page_down)
        self.back_btn.pack(side=RIGHT, padx=5)
        self.back_btn.disable()

        self.master.bind("<Key>", self.on_bind)  # Подключение горячих клавиш
        self.entry.bind("<FocusIn>", self.focusinentry)
        self.entry.bind("<FocusOut>", self.focusoutentry)


    def search(self, event=None):
        """Выводит все объекты удовлетворяющий введеной строке в поле Entry\n
        event - своеобразная заглушка для привязки к Enter"""
        filter = self.entry.get() if self.entry.get() != "Поиск..." else ""
        self.obj_on_page = func.page_distribution(filter, self.login)

        # =========== корректировка вывода =====================
        self.button_frame.destroy()
        self.button_frame = Frame(self.main_frame)
        self.button_frame.pack()
        self.show_objects(self.obj_on_page[0])

        self.active_page = 1
        self.status.config(text=f"Страница {self.active_page} из {len(self.obj_on_page)}")
        self.back_btn.disable()  # кнопка назад
        if self.active_page == len(self.obj_on_page):  # кнопка далее
            self.next_btn.disable()
        else:
            self.next_btn.enable()

    def add_new(self):
        """Добавляет новый обект"""
        new = Note(['', '', '', None], self.search, self.login)
        new.open_window(master=self.master)

    def page_up(self):
        """Перелистывает на следующую страницу"""
        # ================= корректировка нижней строчки ==================
        self.active_page += 1
        self.status.config(text=f"Страница {self.active_page} из {len(self.obj_on_page)}")

        # кнопка далее
        if self.active_page == len(self.obj_on_page):
            self.next_btn.disable()
        else:
            self.next_btn.enable()

        self.back_btn.enable()  # кнопка назад
        self.button_frame.destroy()
        self.button_frame = Frame(self.main_frame)
        self.button_frame.pack()
        self.show_objects(self.obj_on_page[self.active_page - 1])

    def page_down(self):
        """Перелистывает на страницу назад"""
        # ================= корректировка нижней строчки ==================
        self.active_page -= 1
        self.status.config(text=f"Страница {self.active_page} из {len(self.obj_on_page)}")

        self.next_btn.enable()  # кнопка далее
        # кнопка назад
        if self.active_page == 1:
            self.back_btn.disable()
        else:
            self.back_btn.enable()
        self.button_frame.destroy()
        self.button_frame = Frame(self.main_frame)
        self.button_frame.pack()
        self.show_objects(self.obj_on_page[self.active_page - 1])

    def start_show(self):
        """Выводит запси на первой странице"""
        self.show_objects(self.obj_on_page[0])

    def show_objects(self, arr: list):
        """Выводит обекты из списка arr на экран"""
        i = 0
        for file in arr:
            if file:
                try:
                    note = Note(func.loading(file[:-5], self.login), self.search, self.login)
                    note.add_button(self.button_frame).grid(row=i // 4, column=i % 4)
                except EOFError:
                    os.remove(f"resources/data/{self.login}/{file}")  # удаляет этот файл
                    showwarning(title="Преупреждение", message="Внимение\nОбнаружен чужеродный файл, для корректоной работы программа перезапустится")
                    # перезапуск приложения
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
            else:
                Buttons(self.button_frame, relief=FLAT, width=20,
                        height=10).grid(row=i // 4, column=i % 4)  # создание пустой кнопки
            i += 1

    def focusinentry(self, event):
        """Функция вызывается при клике на entry. Убирает фоновую надпись"""
        if self.entry.get() == 'Поиск...':
            self.entry.delete(0, "end")
            self.entry.insert(0, '')
            self.entry.config(fg = 'black')

    def focusoutentry(self, event):
        """Фунция вызывается при удалении курсура с entry. Возвращает фоновую надпись."""
        if self.entry.get() == '':
            self.entry.insert(0, 'Поиск...')
            self.entry.config(fg = 'grey')

    def on_bind(self, event):
        """Вызывается при нажатии любой клавиши. Если это горячие сочетания,
         то вызывает эту функцию, иначе вызывает search()"""
        if (event.state & 4 > 0):
            symbol = chr(event.keycode)
            if symbol == "A":
                self.selectall_rus(event)
            elif symbol == "X":
                self.cut_rus(event)
            elif symbol == "C":
                self.copy_rus(event)
            elif symbol == "V":
                self.past_rus(event)
        else:
            self.search()


class ChildWindow:
    """Класс дочерних окон."""

    def __init__(self, parent: Tk or Toplevel, width: int, height: int, name: str):
        """Создает дочернее окно от аргумента parent.
        При инициализации имеет аргумент по умаолчанию name='Password Manager'
        Сразу установлены размеры окна и иконка. Фокусировка перелючается на данное окно.
        Автоматически создается 2 пространтсва: Освновное и для нижних кнопок.
        А также базовый кнопки: close_btn и ok_btn(без привязки к функциям!)"""
        self.root = Toplevel(parent)
        self.root.title(name)
        self.root.iconbitmap(func.resource_path("resources/icon.ico"))
        self.root.geometry(
            f"{width}x{height}+{self.root.winfo_screenwidth() // 2 - (width // 2)}+{self.root.winfo_screenheight() // 2 - (height // 2)}"
        )
        self.root.resizable(False, False)

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

    def copy_rus(self, event):
        """Функция копирования. Активируется Ctrl+С"""
        if isinstance(event.widget, Entry) and hex(GetKeyboardLayout()) != "0x4090409":
            try:
                ppc.copy(event.widget.selection_get())
            except TclError:
                pass

    def selectall_rus(self, event):
        """Функция выделения всего. Активируется Ctrl+Ф"""
        if isinstance(event.widget, Entry) and hex(GetKeyboardLayout()) != "0x4090409":
            self.master.after(10, lambda w: w.selection_range(0, END), event.widget)
            event.widget.icursor(END)

    def past_rus(self, event):
        """Функция вставления текста. Активируется Ctrl+М"""
        if isinstance(event.widget, Entry) and hex(GetKeyboardLayout()) != "0x4090409":
            try:
                event.widget.delete(SEL_FIRST, SEL_LAST)
                event.widget.insert(INSERT, ppc.paste())
            except TclError:
                event.widget.insert(INSERT, ppc.paste())

    def cut_rus(self, event):
        """Функция вырезки текста. Активируется Ctrl+Ч"""
        if isinstance(event.widget, Entry) and hex(GetKeyboardLayout()) != "0x4090409":
            try:
                ppc.copy(event.widget.selection_get())
                event.widget.delete(SEL_FIRST, SEL_LAST)
            except TclError:
                pass


class NoteWindow(ChildWindow):
    """Дочерний класс от класса ChildWindow. Конфигупрация виджетов для Note"""

    def __init__(self, parent: Tk, name: str, **commands):
        """Аргумент **commands должен ссылки на функции прявязаных к именам: del_command, ok_command, close_command, choose_command"""
        ChildWindow.__init__(self, parent, 500, 325, name)

        # Коррекитровка нижних кнопок
        self.del_btn = Buttons(self.button_frame, text='Удалить',
                               activebackground='red', command=commands['del_command'])  # кнопка Удалить
        self.del_btn.pack(anchor=W, padx=15, pady=10)

        self.ok_btn.config(text="Сохранить", command=commands['ok_command'])  # кнопка Сохранить

        self.close_btn.config(command=commands['close_command'])  # кнопка Закрыть

        # иконка
        icon_frame = Frame(self.main_frame)
        icon_frame.pack(fill=X, pady=10, padx=50)

        self.image_lbl = Label(icon_frame)
        self.image_lbl.pack(side=LEFT)

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

        Label(self.main_frame).pack(side=LEFT, padx=65)  # отступ
        Button(self.main_frame, text="Выбрать иконку", command=commands['choose_command']).pack(
            side=LEFT)  # кнопка для выбора иконки
        Buttons(self.main_frame, text='Сгенерировать пароль',
                command=self.open_generate_window).pack(side=LEFT, padx=10)  # кнопка для генерации пароля
        self.root.bind("<Key>", self.on_bind)  # подключение горячик клавиш

    def update_icon(self, dir_image: str or None):
        """Обновляет иконку. Показывает изображение находящееся по пути dir_image. \n
        Если же в качетсве аргумента передан None, то будет отображаться lock.png"""
        if dir_image:  # если путь к изображению существует
            img = PilImage.open(dir_image)
            self.photoimage = ImageTk.PhotoImage(img)
        else:  # иначе загружаем картинку поумолчанию lock.png
            img = PilImage.open(func.resource_path('resources/lock.png'))
            self.photoimage = ImageTk.PhotoImage(img)

        self.image_lbl.config(image=self.photoimage)  # отображение картинки

    def open_generate_window(self):
        """Открывает окно с генерацией пароля"""
        global state_past
        GenerateWindow(self.root)
        if state_past:  # если новый пароль хотят сохранить
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

    def insert_text(self, **messages):
        """Вставляет текст в указанные Entry. Аргумент **messages может приимать строки 
        привязаных к именнам name, nickname, password."""
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

    def on_bind(self, event):
        """Вызывается при нажатии любой клавиши. Если это горячие сочетания,
         то вызывает эту функцию."""
        if (event.state & 4 > 0):
            symbol = chr(event.keycode)
            if symbol == "A":
                self.selectall_rus(event)
            elif symbol == "X":
                self.cut_rus(event)
            elif symbol == "C":
                self.copy_rus(event)
            elif symbol == "V":
                self.past_rus(event)


class GenerateWindow(ChildWindow):
    """Дочерний класс от класса ChildWindow. Конфигупрация виджетов для GeneratePassword"""

    def __init__(self, parent: Toplevel):
        ChildWindow.__init__(self, parent, 500, 300, "Generate Password")

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
        self.len_password = Scale(password_frame, length=150, orient=HORIZONTAL, from_=4, to=30, command=self.update)
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
        """Включает все флаги, но не выбирает их, и генерирует новый пароль"""
        for name, variable in self.variables:
            check_btn = self.checkbuttons[name]
            check_btn.config(state='normal')
        self.update()

    def check_flag(self):
        """Проверяет корректность флагов.
        \n Если пользователь выключает последний флаг, то включается флаг Lowercase.
        Генерируется новый пароль."""
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
        state_past = True  # дает сигнал что нужно всталять пароль в entry
        self.root.destroy()


class Note:
    """Класс обектов содержащих все записи. Имеет методы для создания окна содержащего всю информацию
    и для добавления кнопки этой записи на главное окошко"""

    def __init__(self, arr: list, update_func, login):
        """инициализации объекта \n
         arr - спиок [name, nickname, password, icon] \n
         update_func - ссылка на функцию search()
         login - пользователь"""
        self.name = arr[0]
        self.nickname = arr[1]
        self.password = arr[2]
        self.icon = arr[3]
        self.disable_del = False
        self.update_func = update_func
        self.login = login

    def add_button(self, master: Tk) -> Buttons:
        """Добавляет инонку записи в окно. И возвращает данную кнопку"""
        self.master = master
        formed_name = self.formatted_name()
        if self.icon:
            try:
                func.check_image_file(self.icon)
                img = PilImage.open(self.icon)
                self.photoimage = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                self.icon = None
                img = PilImage.open(func.resource_path('resources/lock.png'))
                self.photoimage = ImageTk.PhotoImage(img)
        else:
            img = PilImage.open(func.resource_path('resources/lock.png'))
            self.photoimage = ImageTk.PhotoImage(img)
        btn = Buttons(master, text=formed_name, activebackground="#CCCCCC", relief=FLAT,
                      width=145, height=155, image=self.photoimage, compound=TOP, command=self.open_window)
        return btn

    def open_window(self, master=None):
        """Открывает окно данной записки.\n
        Аргумент master нужен для функции add_new(), т.к. она не вызывает аргумент add_button"""
        if master:
            self.password_window = NoteWindow(master, self.name, del_command=self.del_note,
                                              ok_command=self.save_note, close_command=self.close_note,
                                              choose_command=self.choose_icon)
        else:
            self.password_window = NoteWindow(self.master, self.name, del_command=self.del_note,
                                              ok_command=self.save_note, close_command=self.close_note,
                                              choose_command=self.choose_icon)

        self.password_window.update_icon(self.icon)  # отображение картинки
        if master or self.disable_del:
            # если объект новый, то удалить его нельзя
            self.password_window.disable_del_button()
            self.disable_del = False
        self.password_window.insert_text(name=self.name, nickname=self.nickname,
                                         password=self.password)  # загрузка текста
        self.password_window.grab_focus()  # запуск

    def formatted_name(self) -> str:
        """Форматирует Note.name для корректного изображения на кнопке"""
        len_string = 0
        name = ''
        for word in self.name.split():
            len_string += len(word)
            if len_string <= 20:
                name += word + ' '
            else:
                len_string = len(word)
                name += '\n' + word + ' '

        return name

    def save_note(self):
        """Сохраняет данные"""
        if self.name != self.password_window.get_name():
            try:
                os.remove(f"resources/data/{self.login}/{self.name}.data")
                self.name = self.password_window.get_name()
            except FileNotFoundError:
                self.name = self.password_window.get_name()
        self.nickname = self.password_window.get_nickname()
        self.password = self.password_window.get_password()
        if self.icon:
            os.rename(self.icon, f"resources/images/{self.login}/{self.name}.png")
            self.icon = f"resources/images/{self.login}/{self.name}.png"
        func.saving([self.name, self.nickname, self.password, self.icon], self.login)
        self.password_window.close_window()
        self.update_func()

    def choose_icon(self):
        """Открывает диалоговое окно для выбора файла"""
        root = Tk()
        root.iconbitmap(func.resource_path("resources/icon.ico"))
        root.withdraw()
        dir_image = askopenfilename(filetypes=(('All images', '*.png;*.jpg;*.jpeg;*.jpe;*JPG;*.gif;*.ico'),
                                               ('PNG', '*.png'),
                                               ('JPEG', '*.jpg;*.jpeg;*.jpe;*JPG'),
                                               ('GIF', '*.gif'),
                                               ('ICO', '*.ico')))
        if dir_image != '':  # если окно не закрыли
            img = PilImage.open(dir_image)
            img = img.resize((100, 100), PilImage.ANTIALIAS)
            name = 'noname' if self.name == '' else self.name
            try:
                img.save(f'resources/images/{self.login}/{name}.png')
            except FileNotFoundError:
                try:
                    os.mkdir(f'resources/images/{self.login}')
                    img.save(f'resources/images/{self.login}/{name}.png')
                except FileNotFoundError:
                    os.mkdir(f'resources/images')
                    os.mkdir(f'resources/images/{self.login}')
                    img.save(f'resources/images/{self.login}/{name}.png')
            self.icon = f'resources/images/{self.login}/{name}.png'
            self.password_window.update_icon(self.icon)

    def del_note(self):
        """Вызывает уточняющий messagebox и удаляет записку при потвержении."""
        answer = askyesno(title="Потверждение удаления",
                          message=f"Вы действительно хотите безвозратно удалить пароль от {self.name}?")
        if answer:
            os.remove(f"resources/data/{self.login}/{self.name}.data")
            try:
                os.remove(f"resources/images/{self.login}/{self.name}.png")
            except FileNotFoundError:
                pass
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
