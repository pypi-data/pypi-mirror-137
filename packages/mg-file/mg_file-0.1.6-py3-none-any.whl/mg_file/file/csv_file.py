from csv import reader, writer
from os import SEEK_END, SEEK_SET
from typing import Union, List

# pip install prettytable
from prettytable import PrettyTable

from .base_file import BaseFile, ConcatData


class CsvFile(BaseFile):
    def __init__(self, name_file: str):
        super().__init__(name_file, ".csv")

    def readFile(self,
                 *,
                 encoding: str = "utf-8",
                 limit: int = 0,
                 miss_get_head=False,
                 delimiter=",",
                 ) -> list[list[str]]:
        """
        :param limit: Лимит чтения записей
        :param miss_get_head: Пропустить чтение заголовка
        :param delimiter: Символ, который будет разделять колонки
        :param encoding: Кодировка
        """
        _res = []
        with open(self.name_file, "r", encoding=encoding) as _csvFile:
            _reader = reader(_csvFile, delimiter=delimiter)

            if limit:  # Если есть лимит для чтения записей
                for _index, _row in enumerate(_reader):
                    if _index < limit:
                        _res.append(_row)
                    else:
                        break
            else:  # Если лимита нет, то читаем все записи
                _res = list(_reader)

            if miss_get_head:  # Если нужно пропустить заголовки
                return _res[1::]

            else:
                return _res

    def readFileAndFindDifferences(self, new_data_find: List[List], funIter) -> bool:  # +
        """
        for new_data, data_file in zip(self.ListStock, DataFile):
            if new_data != data_file:
                funIter(new_data)

        :param new_data_find: Новые данные
        :param funIter: Функция которая будет выполняться на каждой итерации
        """
        data_file = self.readFile(miss_get_head=True)
        if data_file != new_data_find:
            for _ in (funIter(new_data) for new_data in new_data_find if new_data not in data_file):
                continue
            return True
        else:
            return False

    def readFileRevers(self, *,
                       limit: int = None,
                       encoding: str = "utf-8",
                       newline: str = ""
                       ) -> List[List[str]]:
        def reversed_lines(file):
            # Generate the lines of file in reverse order
            part = ''
            for block in reversed_blocks(file):
                for c in reversed(block):
                    if c == '\n' and part:
                        yield part[::-1]
                        part = ''
                    part += c
            if part:
                yield part[::-1]

        def reversed_blocks(file, block_size=4096):
            # Generate blocks of file's contents in reverse order.
            file.seek(0, SEEK_END)
            here = file.tell()
            while 0 < here:
                delta = min(block_size, here)
                here -= delta
                file.seek(here, SEEK_SET)
                yield file.read(delta)

        res = []
        with open(self.name_file, "r", encoding=encoding, newline=newline) as f:

            if limit:  # Лимит чтения строк
                for row in reader(reversed_lines(f)):
                    if limit:
                        res.append(row)
                        limit -= 1
                    else:
                        break
            else:
                for row in reader(reversed_lines(f)):
                    res.append(row)
        return res

    def writeFile(self,
                  data: Union[list[Union[str, int, float]],
                              list[list[Union[str, int, float]]]],
                  *,
                  header: tuple = None,
                  FlagDataConferToStr: bool = False,
                  encoding: str = "utf-8",
                  delimiter=",",
                  newline="",
                  ):
        """
        @param data:
        @param header: Эти данные будут заголовками
        @param FlagDataConferToStr: Переводит все данные в формат str
        @param delimiter: Символ, который будет разделять колонки
        @param encoding: Кодировка
        @param newline:
        """
        with open(self.name_file, "w", encoding=encoding, newline=newline) as _csvFile:
            _writer = writer(_csvFile, delimiter=delimiter)

            if header:  # Запись заголовка
                _writer.writerow(header)

            if FlagDataConferToStr:
                if type(data[0]) != list:
                    data = [str(n) for n in data]
                else:
                    data = [[str(n) for n in m] for m in data
                            # Проверить что объект можно перебрать
                            if getattr(m, "__iter__", False)]

            if type(data[0]) != list:
                _writer.writerow(data)
            else:
                _writer.writerows(data)

    def appendFile(self, data: Union[list[Union[str, int, float]],
                                     list[list[Union[str, int, float]]]],
                   *,
                   FlagDataConferToStr: bool = False,
                   encoding: str = "utf-8",
                   delimiter=",",
                   ):
        """
        :param data:
        :param FlagDataConferToStr: Переводит все данные в формат str
        :param delimiter: Символ, который будет разделять колонки
        :param encoding: Кодировка
        """
        ConcatData(
            lambda _data: self.writeFile(_data,
                                         FlagDataConferToStr=FlagDataConferToStr,
                                         encoding=encoding,
                                         delimiter=delimiter),
            self.readFile(),
            data)

    @staticmethod
    def ptabel(data: list, align="l"):
        """
        :param data:
        :param align:
        :return:
        """
        x = PrettyTable(data[0])
        x.add_rows(data[1:])
        x.align = align
        return x
