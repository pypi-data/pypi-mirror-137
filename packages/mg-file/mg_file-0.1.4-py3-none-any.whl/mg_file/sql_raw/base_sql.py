from collections import namedtuple
from typing import Callable, Any

# Необходимо переопределить
CONNECT: Callable | object | None = None
ERROR: BaseException | None = None
MUTABLE_COMMAND_A: Callable[[Any, str, tuple | dict | list], Any] | None = None
READ_COMMAND_A: Callable[[Any, str, tuple | dict | list], Any] | None = None
# Переопределится в функции `Config`
SETTINGS_DB: dict | None = None


###########################################
def dictfetchall(cursor) -> list[dict[str, Any]]:
    """
    Вернуть в виде словаря
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def namedtuplefetchall(cursor) -> list[namedtuple]:
    """
    Вернуть в виде именовано го картежа
    """
    desc = cursor.description
    nt_result = namedtuple('_', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def getDataFromType(_cursor: Any, tdata: str) -> Any:
    """
    Вызвать функцию сериализатор на основе `tdata`
    """
    match tdata:
        case "d":
            return dictfetchall(_cursor)
        case "o":
            # Первый элемент
            return _cursor.fetchone()
        case "a":
            return _cursor.fetchall()
        case "n" | None:
            return namedtuplefetchall(_cursor)
