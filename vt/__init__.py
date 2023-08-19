from . import client  # noqa
from . import env  # noqa
from typing import Any


class VT:
    def __init__(self, *_: Any, **__: Any):
        self.env = env.Env()
        self.client = client.Client(self.env.url, self.env.key)

    def checkip(self, ip: str, *args: Any, **kwargs: Any) -> Any:
        return self.client.request("get", "/ip_addresses", str(ip), *args, **kwargs)
