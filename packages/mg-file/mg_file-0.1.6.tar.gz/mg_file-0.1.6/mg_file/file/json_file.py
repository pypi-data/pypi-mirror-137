from json import load, dump
from typing import Any, Union

from .base_file import BaseFile, ConcatData


class JsonFile(BaseFile):
    """
    Работа с Json файлами
    """

    def __init__(self, name_file: str):
        BaseFile.__init__(self, name_file, ".json")

    def readFile(self, **kwargs) -> Union[list, dict, int, str, float, None, bool]:
        with open(self.name_file, "r") as _jsonFile:
            return load(_jsonFile)

    def writeFile(self, data: Union[list, dict, int, str, float, None, bool, tuple],
                  *, indent=4,
                  skipkeys=False,
                  sort_keys=True,
                  ensure_ascii: bool = False):
        """
        :param data: list, dict, int, str, float, None, bool, tuple.
        :param skipkeys: Если False вызовет исключение при неправильном типе данных.
        :param indent: Отступы для записи.
        :param sort_keys: Сортировать ключи.
        :param ensure_ascii: Экранировать символы, если False данные запишутся как есть.
        """
        with open(self.name_file, "w") as _jsonFile:
            dump(data, _jsonFile, skipkeys=skipkeys, sort_keys=sort_keys, indent=indent, ensure_ascii=ensure_ascii)

    def appendFile(self, data: Union[list, dict[str, Any]], *, ensure_ascii: bool = False):
        ConcatData(
            lambda _data: self.writeFile(_data, ensure_ascii=ensure_ascii),
            self.readFile(),
            data)
