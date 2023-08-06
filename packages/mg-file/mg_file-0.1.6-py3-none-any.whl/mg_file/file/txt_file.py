from typing import Dict, Union, Any

from .base_file import BaseFile


class TxtFile(BaseFile):
    """
    Открывать текстового файла в текстовом и БИНАРНОМ виде на
    - чтение
    - запись
    - до записи стандартную
    """

    def __init__(self, name_file: str, *, mod: str = None, encoding: str = None, data: Any = None):
        super().__init__(name_file, ".txt")
        if mod:
            self.res = {
                "r": lambda: self.readFile(encoding=encoding),
                "w": lambda: self.writeFile(data=data),
                "rb": lambda: self.readBinaryFile(),
                "wb": lambda: self.writeBinaryFile(data=data),
                "a": lambda: self.appendFile(data=data),
                "ab": lambda: self.appendBinaryFile(data=data)
            }[mod]()

    def readFileToResDict(self, *args: str, separator: str = '\n') -> Dict[str, str]:
        """
        :param separator:
        :param args: Имя ключей словаря
        """
        resDict: Dict[str, str] = {}
        with open(self.name_file, "r") as f:
            for index, line in enumerate(f):
                resDict[args[index]] = line.replace(separator, "")
        return resDict

    def readFile(self, limit: int = 0, *, encoding: str = None) -> str:  # +
        with open(self.name_file, "r", encoding=encoding) as f:
            if limit:
                res: str = ""
                for line in f:
                    if limit:
                        res += line
                        limit -= 1
                    else:
                        break
                return res
            else:
                return f.read()

    def searchFile(self, name_find: str) -> bool:
        res = False
        with open(self.name_file, "r") as f:
            for line in f:
                if line.find(name_find) != -1:
                    res = True
                    break
        return res

    def readBinaryFile(self) -> bytes:  # +
        with open(self.name_file, "rb") as f:
            return f.read()

    def writeFile(self, data: str):  # +
        with open(self.name_file, "w") as f:
            f.write(data)

    def writeBinaryFile(self, data: Union[bytes, memoryview]):  # +
        with open(self.name_file, "wb") as f:
            f.write(data)

    def appendFile(self, data: str):  # +
        with open(self.name_file, "a") as f:
            f.write(data)

    def appendBinaryFile(self, data: bytes):  # +
        with open(self.name_file, "ab") as f:
            f.write(data)
