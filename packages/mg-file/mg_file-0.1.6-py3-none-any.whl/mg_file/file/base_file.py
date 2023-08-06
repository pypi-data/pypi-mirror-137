from abc import abstractmethod
from hashlib import sha256
from os import makedirs, remove, mkdir
from os.path import abspath, dirname, exists, getsize, splitext
from shutil import rmtree
from typing import Any, Callable

T_ConcatData = list[str | int | float] | list[list[str | int | float]] | dict | set | str


class BaseFile:
    """

    """
    __slots__ = "name_file"

    def __init__(self, name_file: str, type_file: str):
        if splitext(name_file)[1] != type_file:  # Проверяем расширение файла
            raise ValueError(f"Файл должен иметь расширение {type_file}")
        self.name_file: str = name_file
        self.createFileIfDoesntExist()

    def createFileIfDoesntExist(self):
        """
        Создать файл если его нет
        """
        if not exists(self.name_file):
            tmp_ = dirname(self.name_file)
            if tmp_:  # Если задан путь из папок
                makedirs(tmp_)  # Создаем путь из папок
                open(self.name_file, "w").close()
            else:  # Если указано только имя файла без папок
                open(self.name_file, "w").close()

    def checkExistenceFile(self) -> bool:  # +
        """
        Проверить существование файла
        """
        return True if exists(self.name_file) else False

    def deleteFile(self):  # +
        """
        Удалить файл
        """
        # Удаление файла
        if self.checkExistenceFile():
            remove(self.route())

    def sizeFile(self) -> int:  # +
        """
        Получить размер файла
        """
        # Размер файла в байтах
        return getsize(self.name_file)

    def route(self) -> str:  # +
        """
        Получить абсолютный путь
        """
        # Путь к файлу
        return abspath(self.name_file)

    def createRoute(self):
        """
        Создать файл по указному пути, если нужно поместить в папки, то они создадутся
        """
        tmp_route: str = ""
        for folder_name in self.name_file.split('/')[:-1]:
            tmp_route += folder_name
            mkdir(tmp_route)
            tmp_route += '/'

    def removeRoute(self):
        """
        Удалить весь путь к файлу
        """
        rmtree(self.name_file.split('/')[1])

    def HashFileSha256(self) -> str:
        """
        Получить хеш сумму файла
        """
        return sha256sum(self.name_file)

    @abstractmethod
    def readFile(self, *arg) -> Any:
        ...

    @abstractmethod
    def writeFile(self, arg: Any):
        ...

    @abstractmethod
    def appendFile(self, arg: Any):
        ...


def ConcatData(callback: Callable, file_data: T_ConcatData, new_data: T_ConcatData):
    """
    Объединить два переменных, если они одинакового типа

    @param new_data: Текущие данные в `Python`
    @param file_data: Данные из файле
    @param callback: Вызовется при успешной проверки типов
    """

    if type(new_data) == type(new_data):
        match new_data:
            case list():
                file_data.extend(new_data)
            case tuple() | str():
                file_data += new_data
            case dict() | set():
                file_data.update(new_data)
            case _:
                raise TypeError("Не поддерживаемый тип")
        callback(file_data)
    else:
        raise TypeError("Тип данных в файле и тип входных данных различны")


def sha256sum(path_file: str):
    """
    Получить хеш сумму файла
    @param path_file: Путь к файлу
    """
    h = sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(path_file, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()
