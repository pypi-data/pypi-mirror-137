"""

"""

from typing import Any, Callable

from .async_base_sql import AsyncBaseSql
from .async_serializer import Efetch


class Config(AsyncBaseSql):
    """
    from sql_raw.async_sql.async_postgres_sql import Config
    from sql_raw.async_sql.async_serializer import Efetch

    # Создать конфигурацию
    db = Config(user="postgres", password="root", database="fast_api")

    # Добавить список задач
    db.extendTask([
        db.rsql("SELECT * FROM пользователь;", tdata=Efetch.dict_),
        db.rsql("SELECT id FROM пользователь;"),
        db.rsql("SELECT * FROM пользователь;"),
    ])

    # Добавить одну задачу
    db.appendTask(db.rsql("SELECT * FROM пользователь;"))

    # Выполнить задачи
    pprint(db.executeTasks())
    """

    def __init__(self, user: str,
                 password: str,
                 database: str | None = None,
                 port: int = 5432,
                 host: str = "localhost"):
        from psycopg2 import OperationalError
        # https://aiopg.readthedocs.io/en/stable/core.html
        from aiopg import connect
        super().__init__(user, password, host)
        self.SETTINGS_DB.update({
            "port": port,
        })
        if database:
            self.SETTINGS_DB["dbname"] = database
        self.SETTINGS_DB = ' '.join([f"{_k}={_v}" for _k, _v in self.SETTINGS_DB.items()])
        self.CONNECT = connect
        self.ERROR = OperationalError

    async def read_command(self, _connection,
                           execute: str,
                           params: tuple | dict | list = (),
                           tdata: Callable = Efetch.all, ) -> Any:
        async with _connection.cursor() as _cur:
            await _cur.execute(execute, params)
            return await tdata(_cur)

    async def mutable_command(self, _connection,
                              execute: str,
                              params: tuple | dict | list = (),
                              ):
        async with _connection.cursor() as _cur:
            await _cur.execute(execute, params)
        return _cur.statusmessage
