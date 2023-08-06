"""

"""

from typing import Callable

from .sync_serializer import Efetch
from .sync_base_sql import SyncBaseSql


class Config(SyncBaseSql):
    def __init__(self, user: str, password: str, dbname: str | None = None,
                 port: int = 3306,
                 host: str = "localhost"):
        from sync_mysql.connector import connect, Error
        super().__init__(user, password, host)
        self.SETTINGS_DB.update({
            "port": port,
            "dbname": dbname,
        })
        self.CONNECT = connect
        self.ERROR = Error

    def mutable_command(self, _connection, execute: str, params: tuple | dict | list, *args,
                        **kwargs):
        """
        Декоратор для выполнения изменяемой SQL команды
        """
        with _connection.cursor() as cursor:
            cursor.execute(execute, params, multi=kwargs["multi"])
            _connection.commit()
        return cursor.statement

    def read_command(self, _connection, execute: str, params: tuple | dict | list = (),
                     tdata: Callable = Efetch.all,
                     *args,
                     **kwargs):
        """
        Декоратор для выполнения чтения из БД
        """
        with _connection.cursor() as cursor:
            cursor.execute(execute, params, multi=kwargs["multi"])
            return tdata(cursor)
