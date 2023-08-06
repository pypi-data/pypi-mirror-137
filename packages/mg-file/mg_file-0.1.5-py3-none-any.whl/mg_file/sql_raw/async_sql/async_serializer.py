from collections import namedtuple
from enum import Enum
from typing import Callable, Any


async def dictfetchall(cursor) -> list[dict[str, Any]]:
    """
    Вернуть в виде словаря
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in await cursor.fetchall()
    ]


async def namedtuplefetchall(cursor) -> list[namedtuple]:
    """
    Вернуть в виде именовано го картежа
    """
    desc = cursor.description
    nt_result = namedtuple('_', [col[0] for col in desc])
    return [nt_result(*row) for row in await cursor.fetchall()]


async def _fetchone(cursor):
    return await cursor.fetchone()


async def _fetchall(cursor):
    return await cursor.fetchall()


class Efetch(Enum):
    dict_: Callable[[Any], list[dict[str, Any]]] = dictfetchall
    namedtuple: Callable[[Any], list[namedtuple]] = namedtuplefetchall
    one: Callable[[Any], Any] = _fetchone
    all: Callable[[Any], Any] = _fetchall
