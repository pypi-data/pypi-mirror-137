from abc import abstractmethod
from asyncio import run, gather
from collections import deque
from pprint import pformat
from typing import Any, Coroutine, Callable

from loguru import logger

from .async_serializer import Efetch
from ..base_sql import BaseSql


class BaseTasks:
    """
    Базовый класс для списка асинхронных задач.
    Используются как примесь к асинхронному классу `AsyncBaseSql`
    """

    def __init__(self):
        self.tasks: deque[Coroutine] = deque()

    @staticmethod
    async def _run(tasks: deque[Coroutine]):
        """Выполнить список задач"""
        return await gather(*tasks)

    def executeTasks(self):
        """Запустить выполнения задач"""
        res = run(self._run(self.tasks))
        self.tasks.clear()
        return res

    def appendTask(self, coroutine: Coroutine):
        """Добавить здание в список"""
        self.tasks.append(coroutine)

    def extendTask(self, coroutine: list[Coroutine] | deque[Coroutine]):
        """Расширить список задач другим списком список"""
        self.tasks.extend(coroutine)


class AsyncBaseSql(BaseSql, BaseTasks):
    """
    Базовый асинхронны класс
    """

    def __init__(self, user: str, password: str,
                 host: str = "localhost"):
        BaseSql.__init__(self, user, password, host)
        BaseTasks.__init__(self)

    async def connect_db(self, fun: Callable, *args, **kwargs) -> Any:
        """
        Так как у нас всегда включен `autocommit` мы
        можем использовать контекстный менеджер `with`
        """
        try:
            async with self.CONNECT(self.SETTINGS_DB) as connection:
                return await fun(connection, *args, **kwargs)
        except self.ERROR as e:
            logger.error(e)
            raise e

    async def rsql(self, execute: str, params: tuple | dict | list = (), tdata: Callable = Efetch.all) -> str:
        """
        Чтение из БД
        """
        return await self.connect_db(self.read_command, execute=execute, params=params, tdata=tdata)

    async def Rsql(self, execute: str, params: tuple | dict | list = (), tdata: Callable = Efetch.all) -> str:
        """
        Чтение из БД с красивым выводом в консоль
        """
        return await self.pprint_deco(self.rsql, execute, params, tdata)

    async def wsql(self, execute: str, params: tuple | dict | list = ()) -> tuple[
        str, tuple | dict | list]:
        """
        Внесение изменений в БД
        """
        return await self.connect_db(self.mutable_command, execute=execute, params=params)

    @staticmethod
    async def pprint_deco(fun: Callable, execute: str,
                          params: tuple | dict | list = (),
                          tdata: Callable = Efetch.all, ) -> str:
        """
        Декоратор для красивого вывода результата функции в консоль
        """
        return pformat(await fun(execute, params, tdata))

    @abstractmethod
    async def read_command(self, _connection, execute: str,
                           params: tuple | dict | list = (),
                           tdata: Callable = Efetch.all):
        """
        Метод для выполнения чтения из БД
        """
        return NotImplemented()

    @abstractmethod
    async def mutable_command(self, _connection, execute: str, params: tuple | dict | list = (), ):
        """
        Метод для выполнения записи в БД
        """
        return NotImplemented()
