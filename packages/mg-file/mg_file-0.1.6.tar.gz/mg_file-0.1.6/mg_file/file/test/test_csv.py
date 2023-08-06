import unittest

from mg_file import CsvFile


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
