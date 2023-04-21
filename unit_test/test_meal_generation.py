import pytest
from web import app, db, bcrypt
from web.models import User, UserCalories, UserCurrentDiet, DietCalories, UserCaloriesOverTime, Meals, MealsLabel
from flask import url_for

@pytest.fixture
def client():
    """
    Create a test client for the app
    """
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    test_client = app.test_client()

    with app.app_context():
        """
        Create all tables
        """
        db.create_all()

    yield test_client

    with app.app_context():
        """
        Drop all tables
        """
        db.session.remove()
        db.drop_all()

@pytest.fixture
def test_meals():
    """
    Create test meals to be used in other tests

    Returns:
        List[Meals]: A list of test meals
    """
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
    """
    Create a test user to be used in other tests

    Params:
        email: The email of the test user
        password: The password of the test user

    Returns:
        The test user
    """
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(name='Test User', email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

# Log in helper
def login_test_user(client):
    """
    Log in the test user

    Params:
        client: The test client

    Returns:
        The test client
    """
    client.post('/login', data=dict(
        email='test@example.com',
        password='test_password'
    ), follow_redirects=True)
    client.post('/finish-account', 
                    data=dict(height = 170, weight=60, age=22,
                    goal='Lose Weight', activity_level='Sedentary', gender='Male'),
                    follow_redirects=True)
    return client

# Test cases for /get-meals route
def test_get_meals_route(client, test_meals):
    """
    Test cases for /get-meals route

    Params:
        client: The test client
        test_meals: The test meals

    Returns:
        None
    """
    with app.app_context():
        # Get the test user
        test_user = create_test_user()
        login_test_user(client)
        # User does not have UserCalories record
        response = client.get('/get-meals')
        assert response.status_code == 302
        assert response.location.endswith('/show-meals')

# Test cases for /show-meals route
def test_show_meals_route(client, test_meals):
    """
    Test cases for /show-meals route

    Params:
        client: The test client
        test_meals: The test meals

    Returns:
        None
    """
    with app.app_context():
        # Get the test user
        test_user = create_test_user()
        login_test_user(client)

        # Test case 1: User does not have UserCurrentDiet record
        response = client.get('/show-meals')
        assert response.status_code == 302
        assert response.location.endswith('/get-meals')

        # Test case 2: User has UserCurrentDiet record
        client.get('/get-meals')
        response = client.get('/show-meals')
        assert response.status_code == 200

# Test cases for /save-meal route
def test_save_meal_route(client, test_meals):
    """
    Test cases to save the meal

    Params:
        client: The test client
        test_meals: The test meals

    Returns:
        None
    """
    with app.app_context():
        # Get the test user
        test_user = create_test_user()
        login_test_user(client)
        client.get('/get-meals')
        client.get('/show-meals')
        response = client.get('/save-meal')
        saved_calories = UserCaloriesOverTime.query.filter_by(user_id=test_user.id).first()
        assert response.status_code == 302
        assert response.location.endswith('/')
        assert saved_calories is not None