import unittest

from mg_file import PickleFile


class TestPickleFile(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.name_file = "test_pickle.pkl"

    def setUp(self):
        self.pk = PickleFile(self.name_file)
        self.pk.deleteFile()

    def test_writeFile_and_readFile(self):
        # Проверка записи данных
        test_data = [
            (1, 2, 3, 4),
            [12, 23, 221],
            ["1231", 12, (2, 22)],
            {213123, 123213},
            {'s1': '213'},
        ]

        for td in test_data:
            self.pk.writeFile(td)
            self.assertEqual(self.pk.readFile(), td)
            self.pk.deleteFile()

        self.pk.deleteFile()

    def test_appendFile(self):
        test_data = [1, 2, 3, 4]
        new_data = [98, 678, 88]
        self.pk.writeFile(test_data)
        self.pk.appendFile(new_data)
        test_data += new_data
        self.assertEqual(self.pk.readFile(), test_data)
