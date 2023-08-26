from . import client  # noqa
from . import env  # noqa
from typing import Any
from collections.abc import Sequence


class VT:
    """
    Main class for the vt api wrapper.
    Comes with a small set of commonly used methods


    Otherwise you can use the vt.client method to invoke direct api calls
    """

    def __init__(self, *_: Any, **__: Any):
        self.env = env.Env()
        self.client = client.Client(self.env.url, self.env.key)

    def checkip(self, ip: str | Sequence[str], *args: Any, **kwargs: Any) -> Any:
        ip = ip if isinstance(ip, str) else ".".join(ip)
        return self.client.get(f"/ip_addresses/{ip}", *args, **kwargs)
