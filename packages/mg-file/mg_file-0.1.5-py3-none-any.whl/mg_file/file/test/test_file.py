import unittest
from os.path import getsize
from typing import List, Dict

from mg_file.file.csv_file import CsvFile
from mg_file.file.json_file import JsonFile
from mg_file.file.pickle_file import PickleFile
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
        w = TxtFile("test.txt", mod="w", data="123123")
        r1 = TxtFile("test.txt", mod="r")
        self.assertEqual(r1.res, "123123")
        w = TxtFile("test.txt", mod="a", data="99")
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


class TestJson(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        # Данные для теста
        self.testlist: List[List, Dict] = [
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


class TestCsvFile(unittest.TestCase):

    def setUp(self):
        self.cvs_file = CsvFile("test.csv")
        self.cvs_file.deleteFile()

    def test_init_(self):
        # Реакция на некорректное им файла
        self.assertRaises(ValueError, CsvFile, "test.txt")

    def test_writeFile_and_readFile(self):
        # Проверка записи и чтения данных cvs файла
        self.cvs_file.writeFile(
            [[1, 23, 41, 5],
             [21, 233, 46, 35],
             [13, 233, 26, 45],
             [12, 213, 43, 56]], FlagDataConferToStr=True, header=("Данныe", "Data", "Числа", "Num"))

        #  Тест на чтение Cvs файла
        self.assertEqual(self.cvs_file.readFile(),
                         [['Данныe', 'Data', 'Числа', 'Num'], ['1', '23', '41', '5'], ['21', '233', '46', '35'],
                          ['13', '233', '26', '45'], ['12', '213', '43', '56']])

        #  Тест на чтение cvs файла с убранами заголовками
        self.assertEqual(self.cvs_file.readFile(miss_get_head=True),
                         [['1', '23', '41', '5'], ['21', '233', '46', '35'],
                          ['13', '233', '26', '45'], ['12', '213', '43', '56']])

        # Тест на личит чтнеия
        self.assertEqual(self.cvs_file.readFile(limit=2),
                         [['Данныe', 'Data', 'Числа', 'Num'], ['1', '23', '41', '5']])

        #  Тест на привышающий лимит чтения
        self.assertEqual(self.cvs_file.readFile(limit=1123),
                         [['Данныe', 'Data', 'Числа', 'Num'], ['1', '23', '41', '5'], ['21', '233', '46', '35'],
                          ['13', '233', '26', '45'], ['12', '213', '43', '56']])

        #  Тест на чтение в обратном порядке
        self.assertEqual(self.cvs_file.readFileRevers(),
                         [['12', '213', '43', '56'], ['13', '233', '26', '45'], ['21', '233', '46', '35'],
                          ['1', '23', '41', '5'], ['Данныe', 'Data', 'Числа', 'Num']])

        # Тест на лимит чтени в обратном порядке
        self.assertEqual(self.cvs_file.readFileRevers(limit=2), [['12', '213', '43', '56'], ['13', '233', '26', '45']])

        #  Тест на привышающий лимит чтения в обратном порядке
        self.assertEqual(self.cvs_file.readFileRevers(limit=111),
                         [['12', '213', '43', '56'], ['13', '233', '26', '45'], ['21', '233', '46', '35'],
                          ['1', '23', '41', '5'], ['Данныe', 'Data', 'Числа', 'Num']])

        self.cvs_file.deleteFile()

    def test_appendFile(self):
        # проверка до записи в файл
        self.cvs_file.deleteFile()

        # Проверка записи с флагом FlagDataConferToStr
        self.cvs_file.writeFile(
            [[1, 23, 41, 5],
             [21, 233, 46, 35],
             [13, 233, 26, 45],
             [12, 213, 43, 56]], FlagDataConferToStr=True, header=("Данные", "Data", "Числа", "Num"))

        self.cvs_file.appendFile([['2323', '23233', '23']])

        self.assertEqual(self.cvs_file.readFile(),
                         [['Данные', 'Data', 'Числа', 'Num'], ['1', '23', '41', '5'], ['21', '233', '46', '35'],
                          ['13', '233', '26', '45'], ['12', '213', '43', '56'], ['2323', '23233', '23']])

    def test_ordinary(self):
        # Тест записи одномерного массива

        self.cvs_file.deleteFile()
        self.cvs_file.writeFile([123, 123, 222, 1, 312, 223, 2], FlagDataConferToStr=True)
        self.cvs_file.writeFile([123, 123, 222, 1, 2], FlagDataConferToStr=True)
        self.cvs_file.writeFile([123, 123, '222', 1], FlagDataConferToStr=True)
        self.cvs_file.writeFile([123, 222, 1, 2])

        self.cvs_file.appendFile([123, 123, 222, 1, 312, 223, 2], FlagDataConferToStr=True)
        self.cvs_file.appendFile([123, 123, 222, 1, 2], FlagDataConferToStr=True)
        self.cvs_file.appendFile([123, 123, '222', 1], FlagDataConferToStr=True)
        self.cvs_file.appendFile(['123', '222', '1', '2'])

        # Тест записи двумерного массива
        self.cvs_file.deleteFile()
        self.cvs_file.writeFile(
            [[123, 123, 222, 1, 312, 223, 2],
             [4123, 1233, 222, 1, 3312, 223, 2],
             ], FlagDataConferToStr=True)
        self.cvs_file.writeFile(
            [[123, 123, 222, 1, 312, 223, 2],
             [4123, 1233, '222', 1, 3312, 223, 2],
             ], FlagDataConferToStr=True)

        self.cvs_file.writeFile(
            [[123, 123, 222, 1, 312, 223, 2],
             [4123, 1233, 222, 1, 3312, 223, 2],
             ])

        self.cvs_file.appendFile(
            [[123, 123, 222, 1, 312, 223, 2],
             [4123, 1233, 222, 1, 3312, 223, 2],
             ], FlagDataConferToStr=True)
        self.cvs_file.appendFile(
            [[123, 123, 222, 1, 312, 223, 2],
             [4123, 1233, '222', 1, 3312, 223, 2],
             ], FlagDataConferToStr=True)

        self.cvs_file.appendFile(
            [[123, 123, 222, 1, 312, 223, 2],
             [4123, 1233, 222, 1, 3312, 223, 2],
             ])

        # Тест Записи Float
        self.cvs_file.writeFile([123.12, 123.43, 222.2, 1.5, 31.2, 22.3, 2.5], FlagDataConferToStr=True)
        self.assertEqual(
            self.cvs_file.readFile(),
            [['123.12', '123.43', '222.2', '1.5', '31.2', '22.3', '2.5']])

        # Тест записи комберированно
        self.cvs_file.writeFile([12, 123.43, 'Hello Привет', '1.5', 31.2, 22.3, 2.5], FlagDataConferToStr=True),
        self.assertEqual(
            self.cvs_file.readFile(),
            [['12', '123.43', 'Hello Привет', '1.5', '31.2', '22.3', '2.5']])

        # Тест Записи Float
        self.cvs_file.writeFile([123.12, 123.43, 222.2, 1.5, 31.2, 22.3, 2.5]),
        self.assertEqual(self.cvs_file.readFile(),
                         [['123.12', '123.43', '222.2', '1.5', '31.2', '22.3', '2.5']])

        #
        # Тест записи комберированно
        self.cvs_file.writeFile([12, 123.43, 'Hello Привет', '1.5', 31.2, 22.3, 2.5]),
        self.assertEqual(self.cvs_file.readFile(),
                         [['12', '123.43', 'Hello Привет', '1.5', '31.2', '22.3', '2.5']])

    def test_readFileAndFindDifferences(self):
        data_file = [['Халява: на IndieGala бесплатно отдают аркадный футбол FootLOL: Epic Fail League',
                      'https://playisgame.com/halyava/halyava-na-indiegala-besplatno-otdayut-arkadnyy-futbol-footlol-epic-fail-league/'],
                     ['Халява: в Steam бесплатно отдают головоломку Landing и платформер Inops',
                      'https://playisgame.com/halyava/halyava-v-steam-besplatno-otdayut-golovolomku-landing-i-platformer-inops/'],
                     ['Халява: в For Honor можно играть бесплатно на выходных',
                      'https://playisgame.com/halyava/halyava-v-for-honor-mozhno-igrat-besplatno-na-vyhodnyh/'],
                     ['Халява: в сплатно раздают классические квесты Syberia I и Syberia II',
                      'https://playisgame.com/halyava/halyava-v-gog-besplatno-razdayut-klassicheskie-kvesty-syberia-i-i-syberia-ii/'],
                     ['Халява: о отдают музыкальный платформер Symphonia',
                      'https://playisgame.com/halyava/halyava-v-gog-besplatno-otdayut-muzykalnyy-platformer-symphonia/'],
                     ['Халява: на IndieGala бесплатно отдают Defense of Roman Britain в жанре защиты башень',
                      'https://playisgame.com/halyava/halyava-na-indiegala-besplatno-otdayut-defense-of-roman-britain-v-zhanre-zaschity-bashen/'],
                     ['Халява: в GOG можно бесплатно забрать подарки в честь WitcherCon',
                      'https://playisgame.com/halyava/haljava-v-gog-mozhno-besplatno-zabrat-podarki-v-chest-witchercon/'],
                     [
                         'Халява: в EGS бесплатно отдают симулятор Bridge Constructor: The Walking Dead и стратегию Ironcast',
                         'https://playisgame.com/halyava/haljava-v-egs-besplatno-otdajut-simuljator-bridge-constructor-the-walking-dead-i-strategiju-ironcast/'],
                     ['Халява: в GOG стартовала бесплатная раздача коллекции Shadowrun Trilogy',
                      'https://playisgame.com/halyava/khalyava-v-gog-startovala-besplatnaya-razdacha-kollektsii-shadowrun-trilogy/'],
                     ['Халява: в Hell Let Loose можно играть бесплатно на выходных',
                      'https://playisgame.com/halyava/khalyava-v-hell-let-loose-mozhno-igrat-besplatno-na-vykhodnykh/'],
                     ['Халява: в EGS бесплатно раздают Horizon Chase Turbo и Sonic Mania',
                      'https://playisgame.com/halyava/khalyava-v-egs-besplatno-razdayut-horizon-chase-turbo-i-sonic-mania/']]
        new_data = [['Халява: на IndieGala бесплатно отдают аркадный футбол FootLOL: Epic Fail League',
                     'https://playisgame.com/halyava/halyava-na-indiegala-besplatno-otdayut-arkadnyy-futbol-footlol-epic-fail-league/'],
                    ['Халява: в Steam бесплатно отдают головоломку Landing и платформер Inops',
                     'https://playisgame.com/halyava/halyava-v-steam-besplatno-otdayut-golovolomku-landing-i-platformer-inops/'],
                    ['Халява: в For Honor можно играть бесплатно на выходных',
                     'https://playisgame.com/halyava/halyava-v-for-honor-mozhno-igrat-besplatno-na-vyhodnyh/'],
                    ['Халява: ОШИБКА классические квесты Syberia I и Syberia II',
                     'https://playisgame.com/halyava/halyava-v-gog-besplatno-razdayut-klassicheskie-kvesty-syberia-i-i-syberia-ii/'],
                    ['Халява: о отдают музыкальный платформер Symphonia',
                     'https://playisgame.com/halyava/halyava-v-gog-besplatno-otdayut-muzykalnyy-platformer-symphonia/'],
                    ['Халява: на IndieGala ERROR отдают Defense of Roman Britain в жанре защиты башень',
                     'https://playisgame.com/halyava/halyava-na-indiegala-besplatno-otdayut-defense-of-roman-britain-v-zhanre-zaschity-bashen/'],
                    ['Халява: в GOG можно бесплатно забрать подарки в честь WitcherCon',
                     'https://playisgame.com/halyava/haljava-v-gog-mozhno-besplatno-zabrat-podarki-v-chest-witchercon/'],
                    [
                        'Халява: в EGS бесплатно отдают симулятор Bridge Constructor: The Walking Dead и стратегию Ironcast',
                        'https://playisgame.com/halyava/haljava-v-egs-besplatno-otdajut-simuljator-bridge-constructor-the-ERROR-dead-i-strategiju-ironcast/'],
                    ['Халява: в GOG стартовала бесплатная раздача коллекции Shadowrun Trilogy',
                     'https://playisgame.com/halyava/khalyava-v-gog-startovala-besplatnaya-razdacha-kollektsii-shadowrun-trilogy/'],
                    ['Халява: в Hell Let Loose можно играть бесплатно на выходных',
                     'https://playisgame.com/halyava/khalyava-v-hell-let-loose-mozhno-igrat-besplatno-na-vykhodnykh/'],
                    ['Халява: в EGS бесплатно раздают Horizon Chase Turbo и Sonic Mania',
                     'https://playisgame.com/halyava/khalyava-v-egs-besplatno-razdayut-horizon-chase-turbo-i-sonic-mania/']]

        tmpList = []
        self.cvs_file.writeFile(data_file, header=("Имя акции", "Ссылка"))
        self.cvs_file.readFileAndFindDifferences(new_data, tmpList.append)
        self.assertEqual(tmpList, [['Халява: ОШИБКА классические квесты Syberia I и Syberia II',
                                    'https://playisgame.com/halyava/halyava-v-gog-besplatno-razdayut-klassicheskie-kvesty-syberia-i-i-syberia-ii/'],
                                   ['Халява: на IndieGala ERROR отдают Defense of Roman Britain в жанре защиты башень',
                                    'https://playisgame.com/halyava/halyava-na-indiegala-besplatno-otdayut-defense-of-roman-britain-v-zhanre-zaschity-bashen/'],
                                   [
                                       'Халява: в EGS бесплатно отдают симулятор Bridge Constructor: The Walking Dead и стратегию Ironcast',
                                       'https://playisgame.com/halyava/haljava-v-egs-besplatno-otdajut-simuljator-bridge-constructor-the-ERROR-dead-i-strategiju-ironcast/']])

    def __del__(self):
        self.cvs_file.deleteFile()


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


if __name__ == '__main__':
    unittest.main()
