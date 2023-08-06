import unittest
from os.path import getsize
from typing import List, Dict, Any

from mg_file import JsonFile


class TestJson(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        # Данные для теста
        self.testlist: list[list[int | float | str] | dict[int | float | str | Any, int | float | Any]] = [
            [1, 2.1, -1, -2.1, "1", "\t", "Qwe", "Фыв"],
            {12: 2, 1: 1, 1.2: 1.3, 13: 1.2, 4.2: 1, -12: 1, 41: -23, -23.1: -2.2, -232.2: 1,
             "Qwe": 1, 15: "Qwe", -21: "Qwe", 12.3: "DewW", -11: "wasd", "quests": -123},
        ]
        self.name_file = "test.json"

    # Этот метод запускаетсья ПЕРЕД каждой функции теста
    def setUp(self) -> None:
        self.testClassJson = JsonFile(self.name_file)
        self.testClassJson.deleteFile()
        self.testClassJson.createFileIfDoesntExist()

    def test_sizeFile(self):
        # Проверка определение размера файла
        self.testClassJson.writeFile(self.testlist, sort_keys=False)
        self.assertEqual(self.testClassJson.sizeFile(), getsize(self.testClassJson.name_file))

    def test_deleteFile_and_checkExistenceFile(self):
        # Проверка удаление файла
        self.assertEqual(self.testClassJson.checkExistenceFile(), True)
        self.testClassJson.deleteFile()
        self.assertEqual(self.testClassJson.checkExistenceFile(), False)

    def test_writeJsonFile_and_readJsonFile(self):
        # Проверка записи в файл разных структур данных
        # List
        self.testClassJson.deleteFile()
        self.testClassJson.createFileIfDoesntExist()
        temples: List = self.testlist[0]
        self.testClassJson.writeFile(temples)
        self.assertEqual(temples, self.testClassJson.readFile())
        # Dict
        self.testClassJson.deleteFile()
        self.testClassJson.createFileIfDoesntExist()
        temples: Dict = {str(k): v for k, v in self.testlist[1].items()}  # все ключи должны быть типа str
        self.testClassJson.writeFile(temples)
        self.assertEqual(temples, self.testClassJson.readFile())

    def test_appendJsonListFile(self):
        # Проверка до записи в файл разных структур данных
        # List
        self.testClassJson.deleteFile()
        self.testClassJson.createFileIfDoesntExist()
        tempers: List = self.testlist[0]
        self.testClassJson.writeFile(tempers)
        self.testClassJson.appendFile(tempers)
        tempers += tempers
        self.assertEqual(tempers, self.testClassJson.readFile())

        # Dict
        self.testClassJson.deleteFile()
        self.testClassJson.createFileIfDoesntExist()
        tempers: Dict = {str(k): v for k, v in self.testlist[1].items()}  # все ключи должны быть типа str
        self.testClassJson.writeFile(tempers)
        self.testClassJson.appendFile(tempers)
        tempers.update(tempers)
        self.assertEqual(tempers, self.testClassJson.readFile())

    def __del__(self):
        self.testClassJson.deleteFile()
