import requests
from host import host, port


def test_basic_request():
    r = requests.get(f'http://{host}:{port}/')
    assert r.status_code == 200
