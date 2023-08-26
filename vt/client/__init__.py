from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry  # noqa
from typing import Any
from enum import Enum, unique


# TODO: make this configurable
@unique
class RetryCodes(Enum):
    TOO_MANY = 429
    SERVER_ERROR = 500
    GATEWAY = 502
    TIMEOUT = 504


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
    @unique
    class Methods(Enum):
        GET = "get"

    def __init__(
        self,
        url: str,
        key: str,
        *_: Any,
        timeout: Time = Time.TWO,
        backoff: Time = Time.HALF_SECOND,
        max_retries: int = 5,
        **kwargs: Any,
    ) -> None:
        # let requests do it's magic
        super().__init__()
        self.host = url or kwargs["url"]
        self.key = key or kwargs["key"]
        self.headers.update(
            {
                "accept": "application/json",
                "x-apikey": self.key,
            }
        )
        adapter = TimeoutAdapter(
            timeout=timeout.value,
            max_retries=Retry(
                total=max_retries,
                status_forcelist=[code.value for code in RetryCodes],
                backoff_factor=backoff.value,
            ),
        )
        self.mount("https://", adapter)
        self.mount("http://", adapter)

    # def request(
    #     self,
    #     method: str,
    #     url: str | Sequence[str],
    #     params: str | Sequence[str] | None=None,
    #     data: dict | None=None,
    #     headers: dict | None=None,
    #     cookies: dict | None=None,
    #     files: dict | None=None,
    #     auth: str | None=None,
    #     timeout: TimeoutAdapter | None=None,
    #     allow_redirects: bool=True,
    #     proxies: Any=None,
    #     hooks: Any=None,
    #     stream: Any=None,
    #     verify: Any=None,
    #     cert: Any=None,
    #     json: dict | None=None,
    # ) -> Any:
    #     # TODO: better map the args here to the requests.client args
    #     url = url if isinstance(url, str) else "/".join(url)
    #     url = url.rstrip("/")
    #     url = url.lstrip("/")
    #     full_url = f"{self.host}/{url}/{params}"
    #     return super().request(method, full_url, **kwargs)
