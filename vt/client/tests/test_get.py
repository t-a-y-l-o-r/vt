from vt.client import Client
from vt.env import Env
import pytest


@pytest.fixture
def client():
    env = Env()
    client = Client(env.url, env.key)
    return client


@pytest.mark.vcr()
def test_googl_ip(client):
    ip = "8.8.8.8"
    response = client.get(f"/ip_addresses/{ip}")
    # if this fails for any reason then the test fails
    data = response.json()
    assert response.status_code == 200, data
