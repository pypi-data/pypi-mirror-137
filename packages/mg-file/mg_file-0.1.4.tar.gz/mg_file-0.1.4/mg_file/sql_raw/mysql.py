"""

"""
# !!!
import sql_raw.base_sql


def mutable_command(_connection, execute: str, params: tuple | dict | list, *args, **kwargs):
    """
    Декоратор для выполнения изменяемой SQL команды
    """
    with _connection.cursor() as cursor:
        cursor.execute(execute, params, multi=kwargs["multi"])
        _connection.commit()
    return cursor.statement


def read_command(_connection, execute: str, params: tuple | dict | list, *args, **kwargs):
    """
    Декоратор для выполнения чтения из БД
    """
    with _connection.cursor() as cursor:
        cursor.execute(execute, params, multi=kwargs["multi"])
        return cursor.fetchall()


try:
    from mysql.connector import connect, Error
    from mysql.connector.abstracts import MySQLConnectionAbstract

    sql_raw.base_sql.CONNECT = connect
    sql_raw.base_sql.ERROR = Error
    sql_raw.base_sql.READ_COMMAND_A = read_command
    sql_raw.base_sql.MUTABLE_COMMAND_A = mutable_command


    def Config(user: str, password: str, dbname: str | None = None,
               port: int = 3306,
               host: str = "localhost"):
        """
        Настройка SQL
        """
        sql_raw.base_sql.SETTINGS_DB = {"host": host,
                                        "port": port,
                                        "user": user,
                                        "dbname": dbname,
                                        "password": password}
except ModuleNotFoundError:
    raise ModuleNotFoundError("Установите `mysql-connector-python`")
