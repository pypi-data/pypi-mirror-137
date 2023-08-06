from pprint import pformat

from loguru import logger

# !!!
import sql_raw.base_sql


def connect_db(fun):
    """
    Декоратор для создать подключение к БД
    """

    def wrapper(*arg, **kwargs):
        try:
            with sql_raw.base_sql.CONNECT(**sql_raw.base_sql.SETTINGS_DB) as connection:
                res = fun(connection, *arg, **kwargs)
            return res
        except sql_raw.base_sql.ERROR as e:
            logger.error(e)
            raise e

    return wrapper


def mutable_command(*args, **kwargs):
    """
    Декоратор для выполнения изменяемой SQL команды
    """

    def wrapper(fun):
        def decorated_function(_connection, *arg, **kwarg) -> str:
            return sql_raw.base_sql.MUTABLE_COMMAND_A(_connection, *fun(*arg, **kwargs), *args, *arg, **kwargs, **kwarg)

        return decorated_function

    return wrapper


def read_command(*args, **kwargs):
    """
    Декоратор для выполнения чтения из БД

    @param tdata: Тип возвращаемого объекта
        - "d" - dictfetchall
        - "n" - namedtuplefetchall
        - "o" - fetchone
        - "a" - fetchall
    """

    def wrapper(fun):
        def decorated_function(_connection, *arg, **kwarg) -> any:
            return sql_raw.base_sql.READ_COMMAND_A(_connection, *fun(*arg, **kwargs), *args, *arg,
                                                   **kwargs, **kwarg)

        return decorated_function

    return wrapper


def pprint_deco(fun):
    """
    Декоратор для красивого вывода результата функции в консоль
    """

    def wrapper(*arg, **kwargs):
        return pformat(fun(*arg, **kwargs))

    return wrapper


@connect_db
@read_command()
def rsql(execute: str, params: tuple | dict | list = ()) -> tuple[str, tuple | dict | list]:
    """
    Чтение из БД
    """
    return execute, params


@pprint_deco
@connect_db
@read_command()
def Rsql(execute: str, params: tuple | dict | list = ()) -> tuple[str, tuple | dict | list]:
    """
    Чтение из БД с красивым выводом в консоль
    """
    return execute, params


@connect_db
@mutable_command()
def wsql(execute: str, params: tuple | dict | list = ()) -> tuple[str, tuple | dict | list]:
    """
    Внесение изменений в БД
    """
    return execute, params
