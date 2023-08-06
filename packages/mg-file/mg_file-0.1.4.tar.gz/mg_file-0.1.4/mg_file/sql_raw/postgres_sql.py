"""

"""
# !!!
import sql_raw.base_sql


def mutable_command(_connection, execute: str, params: tuple | dict | list, *args, **kwargs):
    """
    Декоратор для выполнения изменяемой SQL команды
    """
    with _connection.cursor() as cursor:
        cursor.execute(execute, params)
        _connection.commit()
    return cursor.statusmessage


def read_command(_connection, execute: str, params: tuple | dict | list = (), *args, **kwargs):
    """
    Декоратор для выполнения чтения из БД
    """
    with _connection.cursor() as cursor:
        cursor.execute(execute, params)
        return sql_raw.base_sql.getDataFromType(cursor, kwargs.get("tdata", None))


try:
    from psycopg2 import connect, OperationalError

    sql_raw.base_sql.CONNECT = connect
    sql_raw.base_sql.ERROR = OperationalError
    sql_raw.base_sql.READ_COMMAND_A = read_command
    sql_raw.base_sql.MUTABLE_COMMAND_A = mutable_command


    def Config(user: str, password: str, database: str | None = None,
               port: int = 5432,
               host: str = "localhost"):
        """
        Настройка SQL
        """
        sql_raw.base_sql.SETTINGS_DB = {"host": host,
                                        "port": port,
                                        "user": user,
                                        "database": database,
                                        "password": password}

except ModuleNotFoundError:
    raise ModuleNotFoundError("Установите `psycopg2-binary`")
