# Описание функционала библиотеки

## TxtFile

Сначала создаем экземпляр класса `TxtFile` а потом работаем с его методами

```python
txt_obj = TxtFile("test.txt")
```

---

- `readFileToResDict(*args: str, separator: str = '\n')-> Dict[str, str]` = Считывает файл и возвращает Dict с ключами
  заданными в параметры `*args` разграничение происходит по параметру
  `separator`

> Пример

```python
txt_obj.writeFile("my name\nmy passwd\nmy token")
res = txt_obj.readFileToResDict("name", "passwd", "token")
assert res == {'name': 'my name', 'passwd': 'my passwd', 'token': 'my token'}
```

---

- `readFile(limit: int = 0, *, encoding: str = None)-> str` = Обычное чтение `.txt` файла. Можно указать лимит по чтение
  строчек `limit`. И кодировку чтения `encoding` значения такие же как и стандартной функции `open()`

> Пример

```python
test_text = "123123\n3123133\n12312d1d12313"
txt_obj.writeFile(test_text)
assert txt_obj.readFile() == "123123\n3123133\n"
```

---

- `searchFile(name_find:str) -> bool` = Поиск слова `name_find` в тексте

> Пример

```python
test_text = "Optional. If the number of \n bytes returned exceed the hint number, \n no more lines will be returned. Default value is  -1, which means all lines will be returned."
txt_obj.writeFile(test_text)
assert txt_obj.searchFile("more") == True
```

---

- `readBinaryFile()->bytes` = Чтение бинарного файла

> Пример

```python
test_str = '123'
txt_obj.writeBinaryFile(test_str.encode())
assert test_str.encode() == txt_obj.readBinaryFile()
```

---

- `writeFile(data:str)` = Запись в тактовом режиме

---

- `appendFile(data: str)` = Добавление в текстовом режиме

---

- `writeBinaryFile(data: Union[bytes, memoryview])` = Запись в бинарном режиме

---

- `appendBinaryFile(data: bytes)` = Добавление данных в бинарный файл

---

## CsvFile

Сначала создаем экземпляр класса `CsvFile` а потом работаем с его методами

```python
csv_obj = CsvFile("test.csv")
```

- `readFile(encoding: str = "utf-8", newline: str = "", limit: int = None, miss_get_head=False) -> List[List[str]]` =
  чтение cvs файла. `encodin newline` стандартной функции `open()`. `limit` сколько строк считать с начало.
  `miss_get_head` вернуть данные без заголовков

> Пример

```python
csv_obj.writeFile(
    [[1, 23, 41, 5],
     [21, 233, 46, 35],
     [13, 233, 26, 45],
     [12, 213, 43, 56]], FlagDataConferToStr=True, header=("Данные", "Data", "Числа", "Num"))

assert csv_obj.readFile() == [['Данные', 'Data', 'Числа', 'Num'],
                              ['1', '23', '41', '5'],
                              ['21', '233', '46', '35'],
                              ['13', '233', '26', '45'],
                              ['12', '213', '43', '56']]
```

---

- `readFileAndFindDifferences(new_data_find: List[List], funIter) -> bool` = Чтение csv файла, с проверкой различий
  входных данных с данными в файле, если такие различия найдены то выполняется переданная функция `funIter`.

> Пример

```python
data_file = [['1', '2'], ['3', '2'], ["today", "Saturday"]]
new_data = [['1', '2'], ['3', '2'], ["today", "Monday"]]
DifferenceList = []
csv_obj.writeFile(data_file, header=("h1", "h2"))
csv_obj.readFileAndFindDifferences(new_data, DifferenceList.append)
assert DifferenceList == [["today", "Saturday"]]
```

---

- `readFileRevers(limit: int = None, encoding: str = "utf-8", newline: str = "") ->  List[List[str]]` = Чтение cvs файла
  с конца в начало.
  `encodin newline` стандартной функции `open()`. `limit` сколько строк считать с конца.

> Пример

```python
csv_obj.writeFile(
    [[1, 23, 41, 5],
     [21, 233, 46, 35],
     [13, 233, 26, 45],
     [12, 213, 43, 56]], FlagDataConferToStr=True, header=("Данные", "Data", "Числа", "Num"))
assert csv_obj.readFileRevers() == [['12', '213', '43', '56'],
                                    ['13', '233', '26', '45'],
                                    ['21', '233', '46', '35'],
                                    ['1', '23', '41', '5'],
                                    ['Данные', 'Data', 'Числа', 'Num']]
```

---

- `writeFile(data: Union[List[Union[str, int, float]], List[List[Union[str, int, float]]]], *, header: tuple = None, FlagDataConferToStr: bool = False, encoding: str = "utf-8", newline: str = "")`
  = Запись данных в csv файл. `encodin newline` стандартной функции `open()`.
  `FlagDataConferToStr` Проверять все входнее данные и конвертировать их в тип `str`. `header` = Задать заголовки
  столбцам.

---

- `appendFile(data: Union[List[Union[str, int, float]], List[List[Union[str, int, float]]]], *, FlagDataConferToStr: bool = False, encoding: str = "utf-8", newline: str = ""
  )` = Добавить данные в конец csv файла. Такие же параметры как у `writeFile.

> Пример

```python
csv_obj.writeFile(
    [[1, 23, 41, 5],
     [21, 233, 46, 35],
     [13, 233, 26, 45],
     [12, 213, 43, 56]], FlagDataConferToStr=True, header=("Данные", "Data", "Числа", "Num"))

csv_obj.appendFile([['2323', '23233', '23']])

assert csv_obj.readFile() == [['Данные', 'Data', 'Числа', 'Num'],
                              ['1', '23', '41', '5'],
                              ['21', '233', '46', '35'],
                              ['13', '233', '26', '45'],
                              ['12', '213', '43', '56'],
                              ['2323', '23233', '23']]
```

---

## JsonFile

Сначала создаем экземпляр класса `JsonFile` а потом работаем с его методами
> Пример

```python
json_obj = JsonFile("test.json")
```

---

- `readFile()` = Чтение данных из json файла

---

- `writeFile(data: Union[List, Dict], *, indent=4, ensure_ascii: bool = False)` = Запись данных в файл, входные
  параметры такие же как у стандартной функции `open()`

---

- `appendFile(data: Union[List, Dict], *, ensure_ascii: bool = False)` = Добавить данные в файл

> Пример

```python
# List
tempers: List = [1, 2, 3, 4]

json_obj.writeFile(tempers)
json_obj.appendFile(tempers)

tempers += tempers
assert tempers == json_obj.readFile()

# Dict
tempers: Dict = {'1': 11, '2': 22, '3'::33}  # Все ключи должны быть типа str

json_obj.writeFile(tempers)
json_obj.appendFile(tempers)

tempers.update(tempers)
assert tempers == json_obj.readFile()
```

---

## PickleFile

Сначала создаем экземпляр класса `PickleFile` а потом работаем с его методами
> Пример

```python
pick_obj = PickleFile("test.pkl")
```

---
-`writeFile( data: Any, *, protocol: int = 3)` = Записать данные в pkl

---
-`readFile()` = Чтение данных phl
> Пример

```python
test_data = [
    (1, 2, 3, 4),
    [12, 23, 221],
    ["1231", 12, (2, 22)],
    {213123, 123213},
    {'s1': '213'},
]
for td in test_data:
    pick_obj.writeFile(td)
    assert pick_obj.readFile() == td
    pick_obj.deleteFile()
```

---
-`appendFile(data:  Union[Tuple, List, Dict, Set], *, protocol: int = 3)` = Добавить данные в pkl
> Пример

```python
test_data = [1, 2, 3, 4]
new_data = [98, 678, 88]
pick_obj.writeFile(test_data)
pick_obj.appendFile(new_data)
test_data += new_data
assert pick_obj.readFile() == test_data
```

---




