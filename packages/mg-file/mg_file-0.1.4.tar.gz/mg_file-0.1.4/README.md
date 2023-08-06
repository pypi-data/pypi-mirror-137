# Что это ?

Это встраемовая библиотека для работы с файлами формата

- txt = [TxtFile](#txtfile)
- csv = [CsvFile](#csvFile)
- json = [JsonFile](#jsonfile)
- pick = [PickleFile](#picklefile)
- SqlLite = [SqlLiteQrm](#sqlLiteqrm)

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

## SqlLiteQrm

```python
sq = SqlLiteQrm('data_base.db')
```

---

- `.name_db` = Получить имя БД

---

- `.header_table[]` = Получить заголовок таблиц из БД

---
> Пример

```python
test_header = {"id": PrimaryKey(int),
               "name": toTypeSql(str),
               "old": NotNullDefault(int, 5),
               "salary": NotNull(float)}
sq.CreateTable('name_table', test_header)
assert sq.header_table['name_table'] == {'id': 'INTEGER PRIMARY KEY',
                                         'name': 'TEXT',
                                         'old': 'INTEGER NOT NULL DEFAULT 5',
                                         'salary': 'REAL NOT NULL'}
```

---

- `ListTables()` = Получить имена всех таблиц в БД

---

- `HeadTable(NameTable, width_table: int = 10)` = Выводи в консоль данные о таблицы из БД. `NameTable` имя таблицы,
  `width_table` ширина столбцов.

> Пример

```python
sq.CreateTable('name_table', {"id": toTypeSql(int), "name": toTypeSql(str), "old": toTypeSql(int)})
print(sq.HeadTable('name_table', 15))
```

---

- `GetTable(NameTable: str, LIMIT: Tuple[int, int] = None, FlagPrint: int = 0)` = Получить данные из таблицы в
  БД. `LIMIT(до, шаг)`, `FlagPrint` Указывает печатать ли результат в консоль

> Пример

```python
test_header = {"id": PrimaryKey(int),
               "name": toTypeSql(str),
               "old": NotNullDefault(int, 5),
               "salary": NotNull(float)}
sq.CreateTable('name_table', test_header)
assert sq.header_table['name_table'],
{'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT', 'old': 'INTEGER NOT NULL DEFAULT 5',
 'salary': 'REAL NOT NULL'})
sq.ExecuteTable('name_table', {"id": 1, "name": "Anton", "old": 30, "salary": 3000.11})
sq.ExecuteTable('name_table', {"id": 2, "name": "Katy", "old": 22, "salary": 3200.23})
assert sq.GetTable('name_table') == [(1, 'Anton', 30, 3000.11), (2, 'Katy', 22, 3200.23)]
```  

--- 

- `GetColumn(NameTable: str, name_columns: str, LIMIT: Tuple[int, int] = None)` = Получить данные из столбца таблицы в
  БД

> Пример

```python
sq.CreateTable(self.name_table,
               {"id": PrimaryKeyAutoincrement(int), "name": toTypeSql(str), "old": toTypeSql(int),
                "sex": NotNullDefault(str, "_")})
sq.ExecuteManyTableDict(self.name_table,
                        [{"name": "Denis", "old": 21},
                         {"name": "Katy", "old": 21, "sex": 1},
                         {"name": "Svetha", "old": 24}]
                        )
assert self.sq.GetColumn(self.name_table, "name") == ['Denis', 'Katy', 'Svetha']
assert self.sq.GetColumn(self.name_table, "old") == [21, 21, 24]
assert self.sq.GetColumn(self.name_table, "old", LIMIT=(2, 0)) == [21, 21]
```

---

- `DeleteTable(NameTable: Union[str, List[str]])` = Удалить одну таблицу или несколько таблиц

---

- `DeleteLineTable(NameTable: str, sqlWHERE: str = "")` = Удалить строки по условию `WHERE`

> Пример

```python
sq.CreateTable('name_table',
               {"id": PrimaryKeyAutoincrement(int), "name": toTypeSql(str), "old": toTypeSql(int),
                "sex": NotNullDefault(str, "_")})
sq.ExecuteManyTableDict('name_table', [{"name": "Denis", "old": 21},
                                       {"name": "Katy", "old": 221, "sex": 1},
                                       {"name": "Mush", "old": 321, "sex": 21},
                                       {"name": "Patio", "old": 231, "sex": 21},
                                       {"name": "Pvetha", "old": 24}])
sq.DeleteLineTable('name_table', "old > 25")
assert sq.GetTable('name_table') == [(1, 'Denis', 21, '_'), (5, 'Pvetha', 24, '_')]
```

---

- `CreateTable(NameTable: str, columns: Union[str, Dict])` = Создать таблицу с заголовками столбцов `columns`.
  Используйте вспомогательные функции из `sqlmodules` для удобного создание sql запросов

> Пример

```python
# Должны содержать уникальные значения
PrimaryKey = lambda TypeColumn: definition(TypeColumn) + " PRIMARY KEY"
# Всегда должно быть заполнено
NotNull = lambda TypeColumn: definition(TypeColumn) + " NOT NULL"
# Все столбцы будут по умолчанию заполнены указанными значениями
NotNullDefault = lambda TypeColumn, default: definition(TypeColumn) + f" NOT NULL DEFAULT {default}"
# Значение по умолчанию
Default = lambda TypeColumn, default: definition(TypeColumn) + " DEFAULT {0}".format(default)
# Авто заполнение строки. подходит для id
PrimaryKeyAutoincrement = lambda TypeColumn: definition(TypeColumn) + " PRIMARY KEY AUTOINCREMENT"
# Конвертация  типа данных python в SQLLite
toTypeSql = lambda TypeColumn: definition(TypeColumn)
```

- `ExecuteTable(NameTable: str, data: Union[str, int, float, List[Union[str, bytes, int, float]], Tuple, Dict[str, Union[str, bytes, int, float]]] = None, sqlRequest: str = "", *, CheckBLOB: bool = False)`
  = Добавить запись в таблицу из БД
  `sqlRequest` вы можете добавить данные из sql запрос.`CheckBLOB` если вы записываете бинарные данные в таблицу
  используйте этот флаг.

> Пример

```python
sq.CreateTable('name_table',
               {"id": toTypeSql(int),
                "old": toTypeSql(int)
                })
test_table: str = 'test_table'
sq.CreateTable(test_table,
               {"old": toTypeSql(int)})

sq.ExecuteManyTable('name_table',
                    [[11, 24],
                     [22, 31],
                     [2312, 312],
                     [231, 68],
                     [344, 187]])

resSQL = Select('name_table', "id").Where("id < 30").Request

sq.ExecuteTable(test_table, sqlRequest=resSQL)

assert sq.GetTable(test_table) == [(11,), (22,)]
```

> Пример `CheckBLOB`

```python
test_header = {"str": toTypeSql(str), "int": toTypeSql(int), "float": toTypeSql(float),
               "bytes": toTypeSql(bytes)}
sq.CreateTable('name_table', test_header)
test_data = ("text", 123, 122.32, b"1011")
sq.ExecuteTable('name_table', test_data, CheckBLOB=True)
assert sq.GetTable('name_table')[0] == test_data
```            

- `ExecuteManyTable(NameTable: str, data: List[Union[List[Union[str, bytes, Binary, int, float]], Tuple]], head_data: Union[List[str], Tuple] = None, *, CheckBLOB: bool = False)`
  = Добавить несколько записей в таблицу в формате List. `head_data` указывать когда длинна входных данных меньше чем
  количество столбцов в таблице

> Пример

```python
sq.CreateTable('name_table', {
    'car_id': PrimaryKeyAutoincrement(int),
    "model": toTypeSql(str),
    "price": toTypeSql(int)
})

car = [
    ("Audi", 432),
    ("Maer", 424),
    ("Skoda", 122)
]
sq.ExecuteManyTable('name_table', car, head_data=("model", "price"))
assert sq.GetTable('name_table') == [(1, 'Audi', 432), (2, 'Maer', 424), (3, 'Skoda', 122)]
```

- `ExecuteManyTableDict(NameTable: str, data: List[Dict])` = Добавить несколько записей в таблицу в формате Dict

> Пример

```python
sq.CreateTable('name_table',
               {"id": PrimaryKeyAutoincrement(int), "name": toTypeSql(str), "old": toTypeSql(int),
                "sex": NotNullDefault(str, "_")})
sq.ExecuteManyTableDict('name_table',
                        [{"name": "Denis", "old": 21},
                         {"name": "Katy", "old": 21, "sex": 1},
                         {"name": "Svetha", "old": 24}]
                        )
assert sq.Search(Select('name_table', "name").Where("old == 21")) == [('Denis',), ('Katy',)]
```

- `UpdateColumne(NameTable: str, name_column: Union[str, List[str]], new_data: Union[str, bytes, int, float, List[Union[str, bytes, int, float]]], sqlWHERE: str = "")`
  = Обновить данные в столбцах таблицы по условию `sqlWHERE`

> Пример

```python
sq.CreateTable('name_table',
               {"id": PrimaryKeyAutoincrement(int), "name": toTypeSql(str), "old": toTypeSql(int),
                "sex": NotNullDefault(str, "_")})
sq.ExecuteManyTableDict('name_table', [{"name": "Denis", "old": 21},
                                       {"name": "Katy", "old": 221, "sex": 1},
                                       {"name": "Mush", "old": 321, "sex": 21},
                                       {"name": "Patio", "old": 231, "sex": 21},
                                       {"name": "Svetha", "old": 24}])

sq.UpdateColumne('name_table', 'old', 99)
assert sq.GetTable('name_table') == [(1, 'Denis', 99, '_'),
                                     (2, 'Katy', 99, '1'),
                                     (3, 'Mush', 99, '21'),
                                     (4, 'Patio', 99, '21'),
                                     (5, 'Svetha', 99, '_')]
```

- `Search` = Поиск данных в таблице
- `SaveDbToFile` = Сохранить БД в отдельный
- `ReadFileToDb`
- `DeleteDb` 









