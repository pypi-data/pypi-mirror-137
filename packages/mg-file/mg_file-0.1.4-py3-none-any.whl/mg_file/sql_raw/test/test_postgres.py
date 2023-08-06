from sql_raw.base_deco import Rsql, wsql
from sql_raw.postgres_sql import Config

Config(user="postgres", password="root", database="fast_api")


def test_read():
    print(Rsql("SELECT * FROM пользователь;"))


def test_write():
    wsql("INSERT INTO пользователь (id,f_name, l_name) VALUES (16,'t', 'd');")


def test_init():
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
    CREATE TABLE фотографии
    (
        id         serial PRIMARY KEY,
        id_user    integer REFERENCES пользователь (id) ON DELETE CASCADE ON UPDATE CASCADE,
        path_image varchar(600)
    );
    INSERT INTO фотографии (id, id_user, path_image)
    VALUES (1, 1, 'http://dummyimage.com/212x100.png/dddddd/000000'),
           (2, 4, 'http://dummyimage.com/170x100.png/cc0000/ffffff'),
           (3, 5, 'http://dummyimage.com/147x100.png/dddddd/000000'),
           (4, 6, 'http://dummyimage.com/122x100.png/5fa2dd/ffffff'),
           (5, 2, 'http://dummyimage.com/222x100.png/dddddd/000000'),
           (6, 4, 'http://dummyimage.com/217x100.png/dddddd/000000'),
           (7, 1, 'http://dummyimage.com/192x100.png/cc0000/ffffff'),
           (8, 9, 'http://dummyimage.com/118x100.png/5fa2dd/ffffff'),
           (9, 6, 'http://dummyimage.com/215x100.png/cc0000/ffffff'),
           (10, 4, 'http://dummyimage.com/235x100.png/ff4444/ffffff');
    """)
