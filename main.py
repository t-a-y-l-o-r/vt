from typing import Any
from collections import defaultdict
from requests import Session
from requests.adapters import HTTPAdapter

TWO_SECONDS = 2
BACKOFF = 0.5


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


class TimeoutAdapter(HTTPAdapter):
    def __init__(self, timeout: float, *args: Any, **kwargs: Any):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, *args: Any, **kwargs: Any) -> Any:
        timeout = kwargs.get("timeout", None)
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(*args, **kwargs)


class Client(Session):
    def __init__(
        self,
        url: str,
        key: str,
        *_: Any,
        timeout: float = TWO_SECONDS,
        backoff: float = BACKOFF,
        **kwargs: Any,
    ) -> None:
        self.host = url or kwargs["url"]
        self.key = key or kwargs["key"]
        self.adapter = TimeoutAdapter(
            timeout=timeout,
            backoff_factor=backoff,
        )


if "__main__" in __name__:
    print("Hello World!")
