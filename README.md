# vt
Simple Wrapper for the Virus Total API

## Configuration
The following env values are _required_:

1. `VT_API_URL`
2. `VT_API_KEY`

vt will attempt to auto-detect these env keys when it first runs loading them into it's configuration.

For details about where to get your api key please see the virus total [documentation](https://developers.virustotal.com/reference/authentication)

## Example usage

### Check IP

```python
from vt import VT

my_vt = VT()

ip_data = my_vt.checkip()
```

### The Client

vt has a client that you can hook into directly.
This client works like a normal `requests` client except that it attempts to handle
the vt specific details for you.

To make a request you can use it like any other `requests` client with one minor exception.
There is an extra argument for

```python
from vt import Client, Env

env = Env()
vt_client = Client(env.url, env.key)

vt_client.request("get", "/ip_addresses", "8.8.8.8", ...)
```

## Contributing

Feel free to submit any contribution PR's if you would like.
However, please note that as of this writing this project is not necessarily intended for general use.
