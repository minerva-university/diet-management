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

# Test function for 'register' route
def test_register(session):
    # Test GET request to 'register' route
    response = session.get(f'http://{host}:{port}/register')
    assert response.status_code == 200

    # Test POST request to 'register' route with valid data
    data = {
        'name': 'New User',
        'email': 'new_user@example.com',
        'password': 'new_password',
        'confirm_password': 'new_password'
    }
    response = session.post(f'http://{host}:{port}/register', data=data)
    assert response.status_code == 200

    # Test POST request to 'register' route with invalid data
    data = {
        'name': 'Invalid User',
        'email': 'invalid_user',
        'password': 'invalid_password',
        'confirm_password': 'invalid_password'
    }
    response = session.post(f'http://{host}:{port}/register', data=data)
    assert response.status_code == 200
    assert b'Invalid email address' in response.content