"""

"""

from typing import Any, Callable

from .sync_base_sql import SyncBaseSql
from .sync_serializer import Efetch


class Config(SyncBaseSql):
    def __init__(self, user: str,
                 password: str,
                 database: str | None = None,
                 port: int = 5432,
                 host: str = "localhost"):
        from psycopg2 import connect, OperationalError
        super().__init__(user, password, host)
        self.SETTINGS_DB.update({
            "port": port,
        })
        if database:
            self.SETTINGS_DB["database"] = database

        self.CONNECT = connect
        self.ERROR = OperationalError

    def read_command(self, _connection,
                     execute: str,
                     params: tuple | dict | list = (),
                     tdata: Callable = Efetch.all) -> Any:
        """
        Декоратор для выполнения чтения из БД
        """
        with _connection.cursor() as cursor:
            cursor.execute(execute, params)
            return tdata(cursor)

    def mutable_command(self, _connection,
                        execute: str,
                        params: tuple | dict | list = (), autocommit: bool = False):
        """
        Декоратор для выполнения изменяемой SQL команды
        """
        # Автоматический коммит
        _connection.autocommit = autocommit
        with _connection.cursor() as cursor:
            cursor.execute(execute, params)
            _connection.commit()
        return cursor.statusmessage
