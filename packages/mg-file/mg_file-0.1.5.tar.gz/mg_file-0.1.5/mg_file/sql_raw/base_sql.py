from typing import Any, Callable


class BaseSql:
    def __init__(self, user: str, password: str,
                 host: str = "localhost"):
        self.SETTINGS_DB: dict[str, Any] = {"host": host,
                                            "user": user,
                                            "password": password}
        self.CONNECT: object | Callable | None = None
        self.ERROR: BaseException | None = None
