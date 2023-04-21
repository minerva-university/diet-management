import requests
from host import host, port
import pytest

@pytest.fixture
def session():
    session = requests.Session()
    yield session
    session.close()

def test_basic_request(session):
    r = session.get(f'http://{host}:{port}/')
    assert r.status_code == 200

def test_register(session):
    url = f'http://{host}:{port}/register'
    data = {'name': 'test', 'email': 'test@example.com', 'password': 'password123', 'confirm_password': 'password123'}
    r = session.post(url, data=data)
    assert r.status_code == 200