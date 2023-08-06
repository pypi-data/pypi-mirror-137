# Пример использование

## `PostgreSQl`

```python
from sql_raw.base_deco import Rsql, wsql
from sql_raw.postgres_sql import Config

Config(user="postgres", password="root", database="ИмяБд$")

wsql("""    
CREATE TABLE пользователь
(
    id     serial PRIMARY KEY,
    f_name varchar(255) NOT NULL,
    l_name varchar(255) NOT NULL
);
INSERT INTO пользователь (id, f_name, l_name)
VALUES (1, 'Carola', 'Yandle'),
       (2, 'Risa', 'Follet'),
       (3, 'Cele', 'Caslin'),
       (4, 'Osgood', 'Demead'),
       (5, 'Roldan', 'Malby'),
       (6, 'Reynard', 'Garlee'),
       (7, 'Erna', 'Vigurs'),
       (8, 'Stewart', 'Naismith'),
       (9, 'Poppy', 'Watling'),
       (10, 'Sybila', 'Teliga');
""")

print(Rsql("SELECT * FROM пользователь;"))
```

# Api

- `rsql`()->`Any` - Получить данные из БД
    - `tdata:str=None` Тип возвращаемого значения
        - "d" - `dictfetchall`
        - "n" - `namedtuplefetchall`
        - "o" - `fetchone`
        - "a" - `fetchall`

- `Rsql`()->`str` - Получить красиво отформатированные данные из БД
    - `tdata:str=None`

- `wsql`() - Записать данные в БД