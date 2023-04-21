import requests
import time


def test_basic_request():
    time.sleep(10)
    r = requests.get('http://172.17.0.1:5000/')
    assert r.status_code == 200
