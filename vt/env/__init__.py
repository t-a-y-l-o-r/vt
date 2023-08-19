from typing import Any
from collections import defaultdict


class Env(dict):
    prefix = "VT"
    url_key = "VT_API_URL"
    api_key = "VT_API_KEY"

    def __init__(self, *_: Any, **__: Any) -> None:
        from os import environ

        self.__env = defaultdict(str)
        for key, value in environ.items():
            if Env.prefix in key:
                self.__env[key] = value
        super().__init__(**self.__env)

    def __getattribute__(self, name: str) -> Any:
        if value := super().get(name, None):
            return value
        return super().__getattribute__(name)

    @property
    def url(self) -> str:
        return self.get(Env.url_key, "")

    @property
    def key(self) -> str:
        return self.get(Env.api_key, "")
