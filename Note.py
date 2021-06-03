'''Содержит классы Note и Buttons'''

from tkinter import Tk, PhotoImage, X, LEFT, FLAT, Button , Entry, Label, Frame, BOTH, RAISED
from tkinter import Toplevel
from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename
from pickle_functions import saving
from os import remove


class Note():
    '''Класс обектов содержащих все записи. Имеет методы для создания окна содержащего всю информацию
    и для добавления кнопки этой записи на главное окошко'''
    def __init__(self, arr):
        ''' функция инициализации объекта
         arr - спиок [name, nickname, password, icon]'''
        self.name = arr[0]
        self.nickname = arr[1]
        self.password = arr[2]
        self.icon = None
        self.disable_del = False


    def add_button(self, master):
        '''добавляет инонку записи'''
        self.master= master
        img = PhotoImage(file= self.icon) if not self.icon is None else None
        btn = Button(master, text= self.name, activebackground= "#CCCCCC", relief= FLAT,
                     width= 20, height= 10, command= self.open_window)
        return btn


    def open_window(self, master= None):
        '''Открывает окно данной записки\n
        аргумент master нужен для функции add_new(), т.к. она не вызывает аргумент add_button'''
        if master is None:
            self.password_window = Toplevel(self.master)
        else:
            self.password_window = Toplevel(master)
        self.password_window.title(self.name)
        self.password_window.iconbitmap("icon.ico")
        self.password_window.geometry(f"500x200+{self.password_window.winfo_screenwidth() // 2 - 250}+{self.password_window.winfo_screenheight() // 2 - 100}")
        self.password_window.grab_set()

        func_frame = Frame(self.password_window, relief=RAISED, borderwidth=1)
        func_frame.pack(fill=BOTH, expand=True)

        # нижние кнопки
        button_frame = Frame(self.password_window)
        button_frame.pack(fill=X, expand=True)

        del_btn = Buttons(button_frame, text='Удалить', activebackground='red', command=self.del_note)
        del_btn.pack(side=LEFT, padx=5, pady=5)
        if (not master is None) or self.disable_del: # если объект новый, то удалить его нельзя
            del_btn.disable()
            self.disable_del = False

        Label(button_frame).pack(side=LEFT, padx=70)

        Buttons(button_frame, text="Сохранить", activebackground='#63DB64',
                command=self.save_note).pack(side=LEFT, padx=15)

        Buttons(button_frame, text="Закрыть", command=self.close_note).pack(side=LEFT)


        # иконка и ее выбор
        icon_frame = Frame(func_frame)
        icon_frame.pack(fill= X)

        if not self.icon is None:
            img = PhotoImage(file= self.icon)
            lbl = Label(icon_frame, image= img)
            lbl.pack(padx= 5, pady= 5, expand= True)
        choose_btn = Button(icon_frame, text= "Выбрать иконку...", command= self.choose_icon)
        choose_btn.pack(expand= True)

        # название
        name_frame = Frame(func_frame)
        name_frame.pack(fill= X)
        name_lbl = Label(name_frame, text="Name:", width=10)
        name_lbl.pack(side=LEFT, padx=5, pady=5)
        self.name_entry = Entry(name_frame)
        self.name_entry.pack(fill=X, padx=5, expand= True)
        self.name_entry.insert(0, self.name)

        # nickname
        nickname_frame = Frame(func_frame)
        nickname_frame.pack(fill= X)
        nickname_lbl = Label(nickname_frame, text="Nickname:", width=10)
        nickname_lbl.pack(side=LEFT, padx=5, pady=5)
        self.nickname_entry = Entry(nickname_frame)
        self.nickname_entry.pack(fill=X, padx=5, expand=True)
        self.nickname_entry.insert(0, self.nickname)

        # password
        password_frame = Frame(func_frame)
        password_frame.pack(fill=X)
        password_lbl = Label(password_frame, text="Password:", width=10)
        password_lbl.pack(side=LEFT, padx=5, pady=5)
        self.password_entry = Entry(password_frame)
        self.password_entry.pack(fill=X, padx=5, expand=True)
        self.password_entry.insert(0, self.password)

        # запуск
        self.password_window.mainloop()


    def save_note(self):
        '''сохраняет данные'''
        if self.name != self.name_entry.get():
            remove(f"data/{self.name}.data")
            self.name = self.name_entry.get()
        self.nickname = self.nickname_entry.get()
        self.password = self.password_entry.get()
        self.icon = self.icon
        saving(self.name, [self.name, self.nickname, self.password, self.icon])
        self.password_window.destroy()


    def choose_icon(self):
        '''открывает диалоговое окно для выбора файла'''
        root= Tk()
        root.iconbitmap("icon.ico")
        root.withdraw()
        self.icon = askopenfilename()


    def del_note(self):
        '''Вызывает уточняющий messagebox и удаляет записку.'''
        answer = askyesno(title= "Потверждение удаления",
                          message=f"Вы действительно хотите безвозратно удалить пароль от {self.name}?")
        if answer:
            remove(f"data/{self.name}.data")
            self.name = ''
            self.nickname = ''
            self.password = ''
            self.icon = None
            self.active_del = True
            self.password_window.destroy()


    def close_note(self):
        '''Вызывает уточняющий messagebox если новые изменения не сохранены.'''
        check_name = self.name == self.name_entry.get()
        check_nickname = self.nickname == self.nickname_entry.get()
        check_password = self.password == self.password_entry.get()
        if check_name and check_nickname and check_password:
            self.password_window.destroy()
        else:
            answer = askyesno(title="Потверждение выхода",
                              message="Вы не сохранили последние изменения.\n           Вы точно хотите выйти?")
            if answer:
                self.password_window.destroy()


class Buttons(Button):
    '''Дочерний класс от класса Button. Имеет дополнительные аргументы:\n
    -disable отключает кнопку\n
    -enable включает кнопку'''
    def disable(self):
        # выключает кнопку
        self.config(state= "disable")


    def enable(self):
        # включает кнопку
        self.config(state= "normal")