from abc import abstractmethod
from os import makedirs, remove, mkdir
from os.path import abspath, dirname, exists, getsize
from shutil import rmtree
from typing import Any, Callable

T_ConcatData = list[str | int | float] | list[list[str | int | float]] | dict | set


class BaseFile:
    """
    Функционал:
        - удаление файла
        - проверка существования файла
        - проверка существования файла и если его нет то создание
        - путь к файлу
        - размер файла
        - проверка разрешения открытия файла
    """
    __slots__ = "name_file"

    def __init__(self, name_file: str):
        self.name_file: str = name_file
        self.createFileIfDoesntExist()

    def createFileIfDoesntExist(self):
        # Создать файл если его нет
        if not exists(self.name_file):
            tmp_ = dirname(self.name_file)
            if tmp_:  # Если задан путь из папок
                makedirs(tmp_)  # Создаем путь из папок
                open(self.name_file, "w").close()
            else:  # Если указано только имя файла без папок
                open(self.name_file, "w").close()

    def checkExistenceFile(self) -> bool:  # +
        # Проверить существование файла
        return True if exists(self.name_file) else False

    def deleteFile(self):  # +
        # Удаление файла
        if self.checkExistenceFile():
            remove(self.route())

    def sizeFile(self) -> int:  # +
        # Размер файла в байтах
        return getsize(self.name_file)

    def route(self) -> str:  # +
        # Путь к файлу
        return abspath(self.name_file)

    def createRoute(self):
        tmp_route: str = ""
        for folder_name in self.name_file.split('/')[:-1]:
            tmp_route += folder_name
            mkdir(tmp_route)
            tmp_route += '/'

    def removeRoute(self):
        rmtree(self.name_file.split('/')[1])

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
    Объединить два переменных одинакового типа
    @param new_data:
    @param file_data:
    @param callback: Вызовется при успешной проверки типов
    """

    if type(new_data) == type(new_data):
        match new_data:
            case list():
                file_data.extend(new_data)
            case tuple():
                file_data += new_data
            case dict() | set():
                file_data.update(new_data)
            case _:
                raise TypeError("Не поддерживаемый тип")
        callback(file_data)
    else:
        raise TypeError("Тип данных в файле и тип входных данных различны")


if __name__ == '__main__':
    pass
