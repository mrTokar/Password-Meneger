"""Содержит функции связанные с работой с файлами"""

from os import listdir, remove, mkdir, path, urandom, rmdir
from PIL import Image
import sys
from hashlib import pbkdf2_hmac


def check_image_file(dir_img: str):
    """Проверяет корректность загружаемой картинки. \n
    Если размер не соответствует 100х100, то удаляет ее."""
    img = Image.open(dir_img)
    if img.size != (100, 100):
        del img
        remove(dir_img)


def check_directory(directoty: str):
    """Проверяет наличие нужных файлов"""
    try:  # проверка resources/images/login
        for file in listdir(f'resources/images/{directoty}'):
            if file[-4:] == '.png':
                check_image_file(f'resources/images/{directoty}/{file}')
            else:
                remove(f'resources/images/{directoty}/{file}')
    except FileNotFoundError:  # если нет нужной дирректории
        try:
            mkdir(f'resources/images/{directoty}')
        except FileNotFoundError:
            mkdir(f'resources/images')
            mkdir(f'resources/images/{directoty}')


def resource_path(relative_path: str):
    """Получает и возвращает абсолютный путь к ресурсу"""
    try:
        # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


def hash_password(password: str, salt=None):
    """Хеширует пароль и возвращает ключ с солью в 16-ричной системе. \n
    Аргумент salt передается набором байтов в 16-ричной систсеме,
    при этом пароль будет хешироваться по переданной соли, иначе сгенрерирует новую"""
    if not salt:
        salt = urandom(32)
    else:
        salt = bytes.fromhex(salt)
    key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key.hex(), salt.hex()


def delete_files(directory: str):
    """Удаляет все файлы из папки"""
    directory = resource_path(directory)
    try:
        
        for file in listdir(directory):
            remove(directory + f"\\{file}")
        rmdir(directory)

    except FileNotFoundError:
        pass
    return directory