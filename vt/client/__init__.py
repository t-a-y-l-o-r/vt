from requests import Session
from requests.adapters import HTTPAdapter
from typing import Any
from enum import Enum, unique


@unique
class Time(Enum):
    TWO = 2
    # TODO is this meant to be a percent?
    HALF_SECOND = 0.5


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
        timeout: Time = Time.TWO,
        backoff: Time = Time.HALF_SECOND,
        **kwargs: Any,
    ) -> None:
        self.host = url or kwargs["url"]
        self.key = key or kwargs["key"]
        self.adapter = TimeoutAdapter(
            timeout=timeout.value,
            backoff_factor=backoff.value,
        )
