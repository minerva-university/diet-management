import requests


def test_basic_request():
    r = requests.get('http://172.17.0.1:5000/')
    assert r.status_code == 200
