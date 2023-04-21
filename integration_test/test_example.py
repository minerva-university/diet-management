import requests


def test_basic_request():
    r = requests.get('http://localhost:5000/')
    assert r.status_code == 200
