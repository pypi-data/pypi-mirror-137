import unittest
from os.path import getsize

from mg_file.file.txt_file import TxtFile


class TestFile(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        # Имя фалйа
        self.name_file = "test.txt"
        # Данные для теста
        self.test_str: str = "ninja cjj,output На двух языках 1#1^23 !23№эЭ123'"

    # Этот метод запускается ПЕРЕД каждой функции теста
    def setUp(self) -> None:
        self.testClassFile = TxtFile(self.name_file)
        self.testClassFile.deleteFile()
        self.testClassFile.createFileIfDoesntExist()

    def test_sizeFile(self):
        # Проверка определение размера файла
        self.testClassFile.writeFile(self.test_str)
        self.assertEqual(self.testClassFile.sizeFile(), getsize(self.testClassFile.name_file))

    def test_deleteFile_and_checkExistenceFile(self):
        # Проверка удаление файла
        self.assertEqual(self.testClassFile.checkExistenceFile(), True)
        self.testClassFile.deleteFile()
        self.assertEqual(self.testClassFile.checkExistenceFile(), False)

    def test_writeFile(self):
        # Проверка записи в файл
        self.testClassFile.writeFile(self.test_str)
        self.assertEqual(self.test_str, self.testClassFile.readFile())

    def test_appendFile(self):
        # Проверка дозaписи в файл
        test_str: str = self.test_str
        self.testClassFile.writeFile(test_str)
        self.testClassFile.appendFile(test_str)
        test_str += test_str
        self.assertEqual(test_str, self.testClassFile.readFile())

    def test_readBinaryFile_and_writeBinaryFile(self):
        # Проверка записи и чтения в двоичном режиме
        self.testClassFile.writeBinaryFile(self.test_str.encode())
        self.assertEqual(self.test_str.encode(), self.testClassFile.readBinaryFile())

    def test_appendBinaryFile(self):
        # Проверка до записи в двоичном режиме
        tests: str = self.test_str
        self.testClassFile.writeBinaryFile(tests.encode())
        self.testClassFile.appendBinaryFile(tests.encode())
        tests += tests
        self.assertEqual(tests.encode(), self.testClassFile.readBinaryFile())

    def test_readFile_Line(self):
        test_text = "123123\n3123133\n12312d1d12313"
        self.testClassFile.writeFile(test_text)
        self.assertEqual(self.testClassFile.readFile(2), "123123\n3123133\n")

    def test_readFileToResDict(self):
        self.testClassFile.writeFile("my name\nmy passwd\nmy token")
        res = self.testClassFile.readFileToResDict("name", "passwd", "token")
        self.assertEqual(res, {'name': 'my name', 'passwd': 'my passwd', 'token': 'my token'})

    def test_searchFile(self):
        test_text = "Optional. If the number of \n bytes returned exceed the hint number, \n no more lines will be returned. Default value is  -1, which means all lines will be returned."
        self.testClassFile.writeFile(test_text)
        self.assertEqual(self.testClassFile.searchFile("more"), True)

    def test___init__QuackCommand(self):
        TxtFile("test.txt", mod="w", data="123123")
        r1 = TxtFile("test.txt", mod="r")
        self.assertEqual(r1.res, "123123")
        TxtFile("test.txt", mod="a", data="99")
        r2 = TxtFile("test.txt", mod="r")
        self.assertEqual(r2.res, "12312399")

    def __del__(self):
        self.testClassFile.deleteFile()


class test_File(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.name_file = "test/test/data/test.txt"

    def test_route(self):
        self.testClassFile = TxtFile(self.name_file)
        self.testClassFile.writeFile("123")
        self.assertEqual(self.testClassFile.readFile(), "123")
        self.testClassFile.removeRoute()


if __name__ == '__main__':
    unittest.main()
