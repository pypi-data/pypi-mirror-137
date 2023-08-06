from pickle import load, dump
from typing import Any, Union

from .base_file import BaseFile


class PickleFile(BaseFile):
    # https://docs.python.org/3/library/pickle.html
    def __init__(self, name_file: str):

        BaseFile.__init__(self, name_file, ".pkl")

    def writeFile(self, data: Any, *, protocol: int = 3):
        # Сериализовать и записать данные в файл
        with open(self.name_file, "wb") as _pickFile:
            dump(data, _pickFile, protocol=protocol)

    def readFile(self, **kwargs) -> Any:
        # Прочитать и десериализация данные из файла
        with open(self.name_file, "rb") as _pickFile:
            return load(_pickFile)

    def appendFile(self, data: Union[tuple, list, dict, set], *, protocol: int = 3):
        tmp_data = self.readFile()

        if type(data) == type(tmp_data):  # Входные данные должны быть такого же типа, что и в файле

            # List
            if type(data) == list:
                tmp_data.extend(data)
                self.writeFile(tmp_data, protocol=protocol)

            # Tuple
            elif type(data) == tuple:
                self.writeFile(tmp_data + data, protocol=protocol)

            # Dict Set
            elif type(data) == dict or type(data) == set:
                tmp_data.update(data)
                self.writeFile(tmp_data, protocol=protocol)

        else:
            raise TypeError("Тип данных в файле и тип входных данных различны")
