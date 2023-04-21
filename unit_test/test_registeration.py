import pytest
from web import app, db, bcrypt
#from web.models import User, UserWeightOverTime
from web.models.User import User
from web.forms import RegistrationForm, LoginForm, CalculateCalories
from flask_login import login_user, current_user, logout_user

# Create a fixture for test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    test_client = app.test_client()
    with app.app_context():
        db.create_all()

    yield test_client

    with app.app_context():
        db.session.remove()
        db.drop_all()

# Helper function to create a test user
def create_test_user(email='test@example.com', password='test_password'):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(name='Test User', email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

# Test function for 'register' route
def test_register(client):
    # Test GET request to 'register' route
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

    # Test POST request to 'register' route with valid data
    response = client.post('/register', data=dict(
        name='New User', email='new_user@example.com', password='new_password', confirm_password='new_password'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Account created for New User!' in response.data

    # Test POST request to 'register' route with invalid data
    response = client.post('/register', data=dict(
        name='Invalid User', email='invalid_user', password='invalid_password', confirm_password='invalid_password'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email address' in response.data

# Test function for 'login' route
def test_login(client):
    # Create a test user
    test_user = create_test_user()

    # Test GET request to 'login' route
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Log In' in response.data

    # Test POST request to 'login' route with valid credentials
    response = client.post('/login', data=dict(
        email='test@example.com', password='test_password'
    ), follow_redirects=True)
    assert response.status_code == 200

    assert b'Please complete your account details.' in response.data

# for 'logout' route
def test_logout(client):
    # Create and login a test user
    test_user = create_test_user()
    with client.session_transaction() as sess:
        sess['user_id'] = test_user.id

    client.post('/login', data=dict(email = 'test@example.com',
                                    password='test_password'), follow_redirects=True)
    # Test GET request to 'logout' route
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data  # Assuming 'Welcome' is part of the content in the 'index' route

# Test function for 'finish_account' route
def test_finish_account(client):
    # Create and login a test user
    test_user = create_test_user()
    with client.session_transaction() as sess:
        sess['user_id'] = test_user.id

    client.post('/login', data=dict(email = 'test@example.com',
                                    password='test_password'), follow_redirects=True)
    # Test GET request to 'finish_account' route
    response = client.get('/finish-account')
    assert response.status_code == 200
    assert b'Complete Account Details' in response.data

    #invalid input
    # Test POST request to 'finish_account' route with invalid data
    response = client.post('/finish-account', data=dict(
        height=0, weight=0, age=0, goal='invalid', activity_level='invalid', gender='invalid'
    ), follow_redirects=True)
    assert response.status_code == 200
    # Assuming 'This field is required' is part of the form validation error messages
    assert b'This field is required' in response.data

    # Test POST request to 'finish_account' route with valid data
    response = client.post('/finish-account', 
                           data=dict(height = 170, weight=60, age=22,
                                     goal='Lose Weight', activity_level='Sedentary', gender='Male'),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Your account has been initialized!' in response.data

    # cannot access finish account for finished accounts
    response = client.post('/finish-account', 
                           data=dict(height = 170, weight=60, age=22,
                                     goal='Lose Weight', activity_level='Sedentary', gender='Male'),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Show Meals' in response.data