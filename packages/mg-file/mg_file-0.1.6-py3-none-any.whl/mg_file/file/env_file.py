from os import environ, getenv
from pprint import pprint
from re import sub

from .txt_file import TxtFile


class EnvFile(TxtFile):

    def __init__(self, name_file: str):
        super(TxtFile, self).__init__(name_file, ".env")
        self.IS_READ_ENV_FILE: bool = False

    def readAndSetEnv(self):
        """
        Чтение переменных окружения из указанного файла, и добавление их в ПО `python`
        """
        with open(self.name_file, 'r', encoding='utf-8') as _file:
            res = {}
            for line in _file:
                tmp = sub(r'^#[\s\w\d\W\t]*|[\t\s]', '', line)
                if tmp:
                    k, v = tmp.split('=', 1)
                    # Если значение заключено в двойные кавычки, то нужно эти кавычки убрать
                    if v.startswith('"') and v.endswith('"'):
                        v = v[1:-1]

                    res[k] = v
        environ.update(res)
        pprint(res)
        self.IS_READ_ENV_FILE = True

    def getEnv(self, name_env: str) -> str:
        """
        Взять переемную окружения, если мы не читали файл с переменными окружения, то вызовется ошибка
        """
        if not self.IS_READ_ENV_FILE:
            raise FileExistsError("Вы не прочитали файл с переменными окружения")
        return getenv(name_env)
