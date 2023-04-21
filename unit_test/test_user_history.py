import pytest
from web import app, db, bcrypt
from web.models import User, UserCalories, UserCurrentDiet, DietCalories, UserCaloriesOverTime, Meals, MealsLabel
from flask import url_for

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

@pytest.fixture
def test_meals():
    meals = [
        Meals(name='Breakfast Meal 1', calories=100, serving_size=1, recipe='Recipe'),
        Meals(name='Breakfast Meal 2', calories=200, serving_size=1, recipe='Recipe'),
        Meals(name='Lunch Meal 1', calories=300, serving_size=1, recipe='Recipe'),
        Meals(name='Lunch Meal 2', calories=400, serving_size=1, recipe='Recipe'),
        Meals(name='Dinner Meal 1', calories=500, serving_size=1, recipe='Recipe'),
        Meals(name='Dinner Meal 2', calories=600, serving_size=1, recipe='Recipe')
    ]
    meals_labels = [
        MealsLabel(meal_id=1, label='breakfast'),
        MealsLabel(meal_id=2, label='breakfast'),
        MealsLabel(meal_id=3, label='lunch'),
        MealsLabel(meal_id=4, label='lunch'),
        MealsLabel(meal_id=5, label='dinner'),
        MealsLabel(meal_id=6, label='dinner')
    ]

    for meal in meals:
        db.session.add(meal)
    for meal_label in meals_labels:
        db.session.add(meal_label)
    db.session.commit()

    return meals

# Helper function to create a test user
def create_test_user(email='test@example.com', password='test_password'):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(name='Test User', email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

# Log in helper
def login_test_user(client):
    client.post('/login', data=dict(
        email='test@example.com',
        password='test_password'
    ), follow_redirects=True)
    client.post('/finish-account', 
                    data=dict(height = 170, weight=60, age=22,
                    goal='Lose Weight', activity_level='Sedentary', gender='Male'),
                    follow_redirects=True)
    return client

def test_show_calories(client, test_meals):
    # Create and login a test user
    create_test_user()
    login_test_user(client)
    client.get('/get-meals')
    client.get('/show-meals')
    client.get('/save-meal')
    client.get('/get-meals')
    client.get('/show-meals')
    client.get('/save-meal')
    # Test GET request to 'show-calories' route
    response = client.get('/show-calories')
    assert response.status_code == 200
    assert b'Calories Over Time' in response.data

    # Test POST request to 'show-calories' route with different time frames
    time_frames = ['1 Week', '2 Weeks', '3 Weeks', '1 Month']
    for time_frame in time_frames:
        response = client.post('/show-calories', data=dict(time=time_frame), follow_redirects=True)
        assert response.status_code == 200
        assert bytes(time_frame, 'utf-8') in response.data

def test_show_weight(client, test_meals):
    # Create and login a test user
    test_user = create_test_user()
    login_test_user(client)
    client.get('/get-meals')
    client.get('/show-meals')
    client.get('/save-meal')
    # Test GET request to 'show-weight' route
    response = client.get('/show-weight')
    assert response.status_code == 200
    assert b'weight Over Time' in response.data

    # Test POST request to 'show-weight' route with different time frames
    time_frames = ['1 Week', '2 Weeks', '3 Weeks', '1 Month', '3 Months', '6 Months', '1 Year']
    for time_frame in time_frames:
        response = client.post('/show-weight', data=dict(time=time_frame), follow_redirects=True)
        assert response.status_code == 200
        assert bytes(time_frame, 'utf-8') in response.data